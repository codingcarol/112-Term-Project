from datetime import date
import datetime
import calendar
from event_functions import *

#I learned datetime functions from CITATION: https://docs.python.org/3/library/datetime.html
#I learned calendar functions from CITATION: https://docs.python.org/3/library/calendar.html
#these functions were used in nearly every function here

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

def get_day_to_weekday_dict(week):
    weekday_dict = {}
    for day in week:
        weekday_dict[day[1].isoformat()] = day[0].lower()
    return weekday_dict

def get_time_index(time):
    time = int(time.split(":")[0])
    return time

def get_nearest_low_time(time):
    time = time.split(":")[0] + ":00"
    return time

def get_nearest_lower_half_hour(time):
    #take a time string, outputs the lowest nearest half hour
    #already in 24 hour time
    minutes = 0
    if ":" in time:
        minutes = int(time.split(":")[1])
    if minutes < 30:
        return time.split(":")[0] + ":00"
    else:
        return time.split(":")[0] + ":30"

def get_nearest_high_time(time):
    time = str(int(time.split(":")[0]) + 1) + ":00"
    return time

def get_nearest_upper_half_hour(time):
    #take a time string, outputs the lowest nearest half hour
    minutes = 0
    if ":" in time:
        minutes = int(time.split(":")[1])
    if minutes <= 30:
        return time.split(":")[0] + ":30"
    else:
        return str(int(time.split(":")[0]) + 1) + ":30"

def get_next_half_hour(time):
    nearest_upper_half_hour = get_nearest_upper_half_hour(time)
    if get_nearest_upper_half_hour(time) == time:
        return get_nearest_high_time(time)
    else:
        return nearest_upper_half_hour 

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
    #checks if the first time is greater than or equal to the second time
    if get_time_index(t1) >= get_time_index(t2):
        return True
    elif (get_time_index(t1) == get_time_index(t2) and 
    int(t1.split(":")[1]) >= int(t2.split(":")[1])):
        return True
    else:
        return False

def is_strictly_time_greater(t1, t2):
    #checks if the first time is greater than or equal to the second time
    if get_time_index(t1) > get_time_index(t2):
        return True
    elif (get_time_index(t1) == get_time_index(t2) and 
    int(t1.split(":")[1]) > int(t2.split(":")[1])):
        return True
    else:
        return False

def times_overlap(t1_start, t1_end, t2_start, t2_end):
    #returns True if the times overlap
    if (is_time_greater(t2_start,t1_start) and 
    is_strictly_time_greater(t1_end, t2_start)):
        return True
    elif (is_strictly_time_greater(t2_end, t1_start) and 
    is_time_greater(t1_end,t2_end)):
        return True
    return False

def duration_time_time(t, duration):
    #adds to duration to time to get the end time
    t_hour, t_minutes = t.split(":")
    duration_hours, duration_minutes = duration.split(":")
    t_hour = int(t_hour)
    t_minutes = int(t_minutes)
    duration_hours = int(duration_hours)
    duration_minutes = int(duration_minutes)
    extra_hour = 0
    new_minutes = t_minutes + duration_minutes
    if new_minutes >= 60:
        extra_hour += 1
        new_minutes %= 60
    new_hour = duration_hours + t_hour + extra_hour
    same_day = True
    if new_hour >= 24:
        new_hour %= 24
        same_day = False
    new_time = f'{new_hour}:{new_minutes}'
    if new_minutes < 10:
        new_time += "0"
    return (same_day, new_time)

def get_half_hour_between(start_time, end_time):
    #gets times between the start and end time very half hour
    start_time = get_nearest_lower_half_hour(start_time)
    end_time = get_nearest_upper_half_hour(end_time)
    if is_time_greater(start_time, end_time):
        return None 
    hour = start_time
    hours = [start_time]
    count = 0
    while hour != end_time and count < 24:
        hour = get_next_half_hour(hour)
        hours.append(hour)
        count += 1
    return hours
'''
def is_time_between(start_date, start_time, end_date, end_time, test_date, test_time):
    #takes strings of date and time and checks if the test date is between the start and end
    start_date = date(start)'''

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
    #I learned calendar functions from CITATION: https://docs.python.org/3/library/calendar.html
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

