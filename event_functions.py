from cmu_112_graphics import *
from date_functions import *
import csv 
from datetime import date

def get_schedule_folder(folder):
    return f'data/{folder}'

def get_flex_events_csv(folder):
    return f'data/{folder}/flexible_events.csv'

def get_recurring_events_csv(folder):
    return f'data/{folder}/recurring_strict_events.csv'

def get_strict_events_csv(folder):
    return f'data/{folder}/strict_events.csv'

def turn_to_strict_event(app, cal_event, date):
    return {'id': cal_event['id'], 'title': cal_event['title'], 'date': date,
    'start_time': cal_event['start_time'], 'end_time': cal_event['end_time'],
    'description': cal_event['description']}

def check_legal_date(start, end, exception, day):
    return (day >= start and day <= end and day not in exception)

def get_week_recurring_events(app, schedule_folder, start_date, end_date):
    events = []
    with open(get_recurring_events_csv(schedule_folder), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        reader = csv.DictReader(csv_file)
        for row in reader:
            recurring_start = date.fromisoformat(row["recurring_start"])
            recurring_end = date.fromisoformat(row["recurring_end"])
            if recurring_start <= end_date:
                exception_days = []
                if row['exceptions'] != "":
                    for d in row["exceptions"].split(','):
                        exception_days.append(date.fromisoformat(d))
                if row['recurrence_type'] == "daily":
                    for day_name, day in app.currentWeek:
                        if check_legal_date(recurring_start, recurring_end, 
                        exception_days, day):
                            events.append(turn_to_strict_event(app, row, 
                            day.isoformat()))
                elif row['recurrence_type'] == "weekly":
                    for day_name, day in app.currentWeek:
                        if check_legal_date(recurring_start, recurring_end, 
                        exception_days, day) and day_name in row['recurrence_time']:
                            events.append(turn_to_strict_event(app, row, 
                            day.isoformat()))
                elif row['recurrence_type'] == "monthly":
                    for day_name, day in app.currentWeek:
                        if check_legal_date(recurring_start, recurring_end, 
                        exception_days, day) and str(day.day) == row['recurrence_time']:
                            events.append(turn_to_strict_event(app, row, 
                            day.isoformat())) 
                elif row['recurrence_type'] == "yearly":
                    for day_name, day in app.currentWeek:
                        if (check_legal_date(recurring_start, recurring_end, 
                        exception_days, day) and 
                        (f'{str(day.month)}-{str(day.day)}' == 
                        row['recurrence_time'])):
                            events.append(turn_to_strict_event(app, row, 
                            day.isoformat())) 
            if recurring_start > end_date:
                break
    return events

def is_later_event(event1, event2):
    d1 = date.fromisoformat(event1['date']) 
    d2 = date.fromisoformat(event2['date'])
    return (d1 > d2 or (d1 == d2 and event1['start_time'] > 
    event2['start_time']))

def merge(a, start1, start2, end):
    #sorting algorithm adapted from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and is_later_event(a[index1], a[index2]))):
            aux[i] = a[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]

def merge_sort_events(cal_events):
    #sorting algorithm adapted from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
    sorted_events = []
    n = len(cal_events)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(cal_events, start1, start2, end)
        step *= 2
    return sorted_events

def construct_strict_schedule(app):
    schedule_folder = app.schedule_folder
    start_date = app.currentWeek[0][1]
    end_date = app.currentWeek[-1][1]
    strict_schedule = []
    with open(get_strict_events_csv(schedule_folder), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        reader = csv.DictReader(csv_file)
        for row in reader:
            d = date.fromisoformat(row["date"])
            if d >= start_date and d <= end_date:
                strict_schedule.append(row)
            if d > end_date:
                break
    recurring_events = get_week_recurring_events(app, schedule_folder, 
    start_date, end_date)
    both_events = strict_schedule + recurring_events #unsorted
    merge_sort_events(both_events) #sort them
    return both_events
   