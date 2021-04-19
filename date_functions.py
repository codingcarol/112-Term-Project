from datetime import date
import datetime
import calendar
from event_functions import *

#CITATION: https://docs.python.org/3/library/datetime.html
#CITATION: https://docs.python.org/3/library/calendar.html

def format_date_string(input_date, date_type):
    if date_type == "day":
        if input_date.day < 10:
            return "0" + str(input_date.day)
        else:
            return str(input_date.day)
    elif date_type == "month":
        if input_date.month < 10:
            return "0" + str(input_date.month)
        else:
            return str(input_date.month)
    elif date_type == "year":
        return str(input_date.year)

def get_current_date():
    return date.today()

def change_current_date(app, year, month, day, useArrowKeys):
    d = nearest_valid_date(app, year, month, day)
    app.currentWeek = get_week(app, d.year, d.month, d.day)
    if useArrowKeys:
        app.currentDate = app.currentWeek[0][1]
    else:
        app.currentDate = d 
    app.calSelectorInputs[0].set_value(app.currentDate.year)
    app.calSelectorInputs[1].set_value(app.currentDate.month)
    app.calSelectorInputs[2].set_value(app.currentDate.day)
    app.schedule = construct_strict_schedule(app)

def get_value_in_range(entry, bounds):
    lower, upper = bounds
    if entry > upper:
        return upper
    elif entry < lower:
        return lower
    else:
        return entry

def last_day_of_month(year, month):
    cal = calendar.Calendar()
    days = [i for i in cal.itermonthdays(year, month) if i != 0]
    return days[-1]

def nearest_valid_date(app, year, month, day):
    year = get_value_in_range(year, app.yearRange)
    month = get_value_in_range(month, app.monthRange)
    day = get_value_in_range(day, (1, last_day_of_month(year, 
    month)))
    return date(year, month, day)

def get_previous_month(month):
    if month <= 1:
        return 12
    else:
        return month - 1

def get_previous_year(year):
    if year <= 2010:
        return None
    else:
        return year - 1

def get_next_month(month):
    if month >= 12:
        return 1
    else:
        return month + 1 

def get_next_year(year):
    if year >= 9999:
        return None
    else:
        return year + 1

def get_week_day_start(app, week):
    return week[0][1]

def get_week_day_end(app, week):
    return week[-1][1]

def get_week_day_index(day):
    return (day.weekday() + 1) % 7

def get_time_index(time):
    time = int(time.split(":")[0])
    return time

def get_nearest_low_time(time):
    time = time.split(":")[0] + ":00"
    return time

def get_nearest_high_time(time):
    time = str(int(time.split(":")[0]) + 1) + ":00"
    return time

def to_24_hr_time(times_list):
    new_times = []
    for t in times_list:
        if "A" in t:
            if "12" in t.split(" ")[0]:
                new_times.append("0:00")
            else:
                new_times.append(t.split(" ")[0])
        else:
            t_index = get_time_index(t.split(" ")[0]) + 12
            if t_index == 24:
                new_times.append(t.split(" ")[0])
            else:
                new_times.append(str(t_index) + ":" + t.split(" ")[0].split(":")[1])
    return new_times

def is_time_greater(t1, t2):
    if get_time_index(t1) >= get_time_index(t2):
        return True
    elif (get_time_index(t1) == get_time_index(t2) and 
    int(t1.split(":")[1]) >= int(t2.split(":")[1])):
        return True
    else:
        return False

def fill_end_week(app, week, year, month):
    if week[0][-1] + 7 > last_day_of_month(year, month): 
        month = get_next_month(month)
        if month == 1:
            year = get_next_year(year)
            if year == None:
                return None
        return get_partial_week(app, year, month, 1)[:7 - len(week)]
    else:
        return get_partial_week(app, year, month, 
        week[0][-1] + 7)[:7 - len(week)]

def fill_start_week(app, week, year, month):
    if week[0][-1] - 7 < 1: 
        month = get_previous_month(month)
        if month == 12:
            year = get_previous_year(year)
            if year == None:
                return None
        return get_partial_week(app, year, month, 28)[len(week) - 7:]
    else:
        return get_partial_week(app, year, month, 
        week[0][-1] - 7)[len(week) - 7:]

def fill_week(app, week, year, month):
    if week[0][-1] == 1 and len(week) < 7:
        start = fill_start_week(app, week, year, month)
        if start == None:
            return week
        return start + week
    elif week[-1][-1] == last_day_of_month(year, month) and len(week) < 7:
        fill_week_end = True
        end = fill_end_week(app, week, year, month)
        if end == None:
            return week
        return week + end
    else:
        return week 

def get_partial_week(app, year, month, day):
#returns a dict of the week, given a year, month, day 
    cal = calendar.Calendar()
    cal.setfirstweekday(app.firstWeekDay)
    days_of_month = [i for i in cal.itermonthdays2(year, month)]
    for i in range(0, len(days_of_month), 7):
        week = days_of_month[i:i+7]
        for day_of_week in week:
            if day == day_of_week[0]:
                name_and_day = []
                for i in range(len(week)):
                    if week[i][0] != 0:
                        name_and_day.append((app.weekdays[i], year, month, 
                        week[i][0]))
                return name_and_day
    return None

def get_week(app, year, month, day):
    week = get_partial_week(app, year, month, day)
    week = fill_week(app, week, year, month)
    new_week = []
    for i in range(len(week)):
        new_week.append((week[i][0], date(week[i][1], week[i][2], week[i][3])))
    return new_week

def get_previous_week_date(app, week):
    if week[0][1].day - 1 < 1:
        month = get_previous_month(week[0][1].month)
        year = week[0][1].year
        if month == 12:
            year = get_previous_year(year)
            if year == None:
                return (week[0][1].year, week[0][1].month, week[0][1].day)
        return (year, month, last_day_of_month(week[0][1].year, 
        week[0][1].month))
    else:
        return (week[0][1].year, week[0][1].month, week[0][1].day - 1)

def get_next_week_date(app, week):
    if week[-1][1].day + 1 > last_day_of_month(week[-1][1].year, 
        week[-1][1].month):
        month = get_next_month(week[-1][1].month)
        year = week[-1][1].year
        if month == 1:
            year = get_next_year(week[-1][1].year)
            if year == None:
                return (week[-1][1].year, week[-1][1].month, week[-1][1].day)
        return (year, month, 1)
    else:
        return (week[-1][1].year, week[-1][1].month, week[-1][1].day + 1)