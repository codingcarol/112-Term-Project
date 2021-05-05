from datetime import date
import datetime
import calendar
from event_functions import *

#I learned datetime functions from CITATION: https://docs.python.org/3/library/datetime.html
#I learned calendar functions from CITATION: https://docs.python.org/3/library/calendar.html
#these functions were used in nearly every function here

def format_date_string(input_date, date_type):
    #formats date string to a two digit string
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
    #returns the todays date
    return date.today()

def change_current_date(app, year, month, day, useArrowKeys):
    #changes the current date
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
    '''
    if value within the bounds -> return value
    if value below the bounds -> return lower bound
    if value above bounds -> return upper bound
    '''
    lower, upper = bounds
    if entry > upper:
        return upper
    elif entry < lower:
        return lower
    else:
        return entry

def last_day_of_month(year, month):
    #return last day of the month 
    cal = calendar.Calendar()
    days = [i for i in cal.itermonthdays(year, month) if i != 0]
    return days[-1]

def nearest_valid_date(app, year, month, day):
    #find the nearest valid date, given numbers for the year month and day
    year = get_value_in_range(year, app.yearRange)
    month = get_value_in_range(month, app.monthRange)
    day = get_value_in_range(day, (1, last_day_of_month(year, 
    month)))
    return date(year, month, day)

def get_previous_month(month):
    #returns int of previous month 
    if month <= 1:
        return 12
    else:
        return month - 1

def get_previous_year(year):
    #returns int of previous year
    if year <= 2010:
        return None
    else:
        return year - 1

def get_next_month(month):
    #returns int of the next month
    if month >= 12:
        return 1
    else:
        return month + 1 

def get_next_year(year):
    #returns int of the next year
    if year >= 9999:
        return None
    else:
        return year + 1

def get_week_day_start(app, week):
    #returns date of the first day in week
    return week[0][1]

def get_week_day_end(app, week):
    #returns date of the last day in the week
    return week[-1][1]

def get_week_day_index(day):
    #given a day, return the day of the week it is as an int
    return (day.weekday() + 1) % 7

def get_day_to_weekday_dict(week):
    '''
    given a week listing, return a dict in the format
    date: day of the week
    '''
    weekday_dict = {}
    for day in week:
        weekday_dict[day[1].isoformat()] = day[0].lower()
    return weekday_dict

def get_time_index(time):
    #gets the index of the time
    time = int(time.split(":")[0])
    return time

def time_is_valid(hours, minutes):
    #returns of the time is valid
    h = int(hours)
    m = int(minutes)
    return (h >= 0 and h <= 24 and m >= 0 and m <= 59)
    
def get_nearest_low_time(time):
    #rounds time down
    time = time.split(":")[0] + ":00"
    if time == ":00":
        return "0:00"
    t_int = int(time.split(":")[0])
    if t_int < 10:
        return str(t_int) + ":00"
    else:
        return str(t_int) + ":00"
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
    #rounds time up to the hour
    time = str(int(time.split(":")[0]) + 1) + ":00"
    return time

def get_nearest_upper_half_hour(time):
    #take a time string, outputs the lowest nearest half hour (rounds to lower half hour)
    minutes = 0
    if ":" in time:
        minutes = int(time.split(":")[1])
    if minutes <= 30:
        return time.split(":")[0] + ":30"
    else:
        return str(int(time.split(":")[0]) + 1) + ":30"

def get_next_half_hour(time):
    #rounds up to nearest half hour
    nearest_upper_half_hour = get_nearest_upper_half_hour(time)
    if get_nearest_upper_half_hour(time) == time:
        return get_nearest_high_time(time)
    else:
        return nearest_upper_half_hour 

def to_24_hr_time(times_list):
    #convers a list of times to the times in a 24 hour format
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

def is_time_greater_or_eq(t1, t2):
    #checks if the first time is greater than or equal to the second time
    if get_time_index(t1) > get_time_index(t2):
        return True
    elif (get_time_index(t1) == get_time_index(t2) and 
    int(t1.split(":")[1]) >= int(t2.split(":")[1])):
        return True
    else:
        return False

def is_strictly_time_greater(t1, t2):
    #checks if the first time is greater than to the second time
    if get_time_index(t1) > get_time_index(t2):
        return True
    elif (get_time_index(t1) == get_time_index(t2) and 
    int(t1.split(":")[1]) > int(t2.split(":")[1])):
        return True
    else:
        return False

def times_overlap(t1_start, t1_end, t2_start, t2_end):
    #returns True if the times overlap
    if (is_time_greater_or_eq(t2_start,t1_start) and 
    is_strictly_time_greater(t1_end, t2_start)):
        return True 
    elif (is_strictly_time_greater(t2_end, t1_start) and 
    is_time_greater_or_eq(t1_end,t2_end)):
        return True
    t1_start, t2_start = t2_start, t1_start
    t1_end, t2_end = t2_end, t1_end
    if (is_time_greater_or_eq(t2_start,t1_start) and 
    is_strictly_time_greater(t1_end, t2_start)):
        return True 
    elif (is_strictly_time_greater(t2_end, t1_start) and 
    is_time_greater_or_eq(t1_end,t2_end)):
        return True
    return False

def add_duration_to_time(t, duration):
    #adds to duration to time to get the end time
    #t and duration format is hours:minutes
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
        new_time = new_time.split(":")[0] + ":0" + new_time.split(":")[1]
    return (same_day, new_time)


def subtract_duration_from_time(t, duration):
    #adds to duration to time to get the end time
    #t and duration format is hours:minutes
    t_hour, t_minutes = t.split(":")
    duration_hours, duration_minutes = duration.split(":")
    t_hour = int(t_hour)
    t_minutes = int(t_minutes)
    duration_hours = int(duration_hours)
    duration_minutes = int(duration_minutes)
    extra_hour = 0
    new_minutes = t_minutes - duration_minutes
    if t_minutes - duration_minutes < 0:
        extra_hour += 1
        new_minutes = 60 - abs(t_minutes - duration_minutes)
    new_hour = t_hour - duration - 5
    same_day = True
    if new_hour >= 24:
        new_hour %= 24
        same_day = False
    new_time = f'{new_hour}:{new_minutes}'
    if new_minutes < 10:
        new_time = new_time.split(":")[0] + ":0" + new_time.split(":")[1]
    return (same_day, new_time)

def find_duration_between(start_time, end_time): #also means subtraction
    #adds to duration to time to get the end time
    #t and duration format is hours:minutes
    #assumes that start and end are the same day
    if is_strictly_time_greater(start_time, end_time): 
        start_time, end_time = end_time, start_time
    start_hour, start_minutes = start_time.split(":")
    end_hour, end_minutes = end_time.split(":")
    start_hour = int(start_hour)
    start_minutes = int(start_minutes)
    end_hour = int(end_hour)
    end_minutes = int(end_minutes)
    extra_hour = 0
    new_minutes = end_minutes - start_minutes
    if start_minutes > end_minutes:
        new_minutes = 60 - abs(end_minutes - start_minutes)
        extra_hour += 1
    new_hour = end_hour - start_hour - extra_hour
    same_day = True
    if new_hour < 0:
        new_hour = 24 + new_hour
        same_day = False
    duration = f'{new_hour}:{new_minutes}'
    if new_minutes < 10:
        duration = duration.split(":")[0] + ":0" + duration.split(":")[1]
    return duration

def get_overlap_time(t1_start, t1_end, t2_start, t2_end):
    #checks if times overlap
    if not times_overlap(t1_start, t1_end, t2_start, t2_end): return None
    if (is_time_greater_or_eq(t2_start,t1_start) and 
    is_strictly_time_greater(t1_end, t2_start)):
        return find_duration_between(t2_start, t1_end)
    elif (is_strictly_time_greater(t2_end, t1_start) and 
    is_time_greater_or_eq(t1_end,t2_end)):
        return find_duration_between(t1_start, t2_end)
    elif (is_time_greater_or_eq(t1_start,t2_start) and 
    is_time_greater_or_eq(t2_end, t1_end)):
        return find_duration_between(t1_start, t1_end)
    elif (is_time_greater_or_eq(t2_start,t1_start) and 
    is_time_greater_or_eq(t1_end, t2_end)):
        return find_duration_between(t2_start, t2_end)
    return None

def get_duration_as_int(t):
    #given an hour:minute duration, returns the time in minutes
    h, m = t.split(":")
    h = int(h)
    m = int(m)
    return h*60 + m

def get_half_hour_between(start_time, end_time):
    #gets times between the start and end time very half hour
    start_time = get_nearest_lower_half_hour(start_time)
    end_time = get_nearest_upper_half_hour(end_time)
    if is_time_greater_or_eq(start_time, end_time):
        return None 
    hour = start_time
    hours = [start_time]
    count = 0
    while hour != end_time and count < 24:
        hour = get_next_half_hour(hour)
        hours.append(hour)
        count += 1
    return hours

def get_times_between(start_time, end_time, duration, include_start):
    #get the times between, returns empty list if goes start_time + duration goes past midnight
    times_between = []
    same_day, current_time_between = add_duration_to_time(start_time, "00:01")
    same_day2, new_end_time = add_duration_to_time(current_time_between, duration)
    if include_start:
        times_between.insert(0, start_time)
    if not same_day: return times_between
    while is_strictly_time_greater(end_time, new_end_time):
        times_between.append(current_time_between)
        same_day, new_time = add_duration_to_time(current_time_between, "00:01")
        same_day2, new_end_time = add_duration_to_time(current_time_between, duration)
        if not same_day:
            break
        current_time_between = new_time
    return times_between

def weave_values(list1, list2):
    #starts with list1 value
    new_list = []
    i = 0
    for i in range((min(len(list1), len(list2)))):
        new_list.append(list1[i])
        new_list.append(list2[i])
    if len(list1) - 1 != i:
        new_list += (list1[i+1:])
    elif len(list2) - 1 != i:
        new_list += (list2[i+1:])
    return new_list

def make_into_time_str(h1, m1):
    #changes the time given hours and minutes into a combined time string
    if h1 < 10:
        h1 = "0" + str(h1)
    else:
        h1 = str(h1)
    if m1 < 10:
        m1 = "0" + str(m1)
    else:
        m1 = str(m1)
    return h1 + ":" + m1
    
def get_times_within_fifteen_min(t):
    #finds the times within fifteen minutes
    #if goes over midnight or before midnight, defaults to 00:00 times
    if is_time_greater_or_eq(t, "00:16"):
        lower_time = find_duration_between(t, "00:15") #lower times
    else:
        lower_time = "00:00"
    same_day, higher_time = add_duration_to_time(t, "00:15")
    if not same_day:
        higher_time = "24:00"
    lowers = get_times_between(lower_time, t, "00:01", True)[::-1]
    highers = get_times_between(t, higher_time, "00:01", True)
    return weave_values(highers, lowers)

def fill_end_week(app, week, year, month):
    #given the first few days in week, returns the rest of the week
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
    #given the last few days of the week, returns the rest of the beginning of the week
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
    #given only some days of a week, gets the other days and combines them to make a 
    #full seven day week
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
    #gets the week given one date
    week = get_partial_week(app, year, month, day)
    week = fill_week(app, week, year, month)
    new_week = []
    for i in range(len(week)):
        new_week.append((week[i][0], date(week[i][1], week[i][2], week[i][3])))
    return new_week

def get_previous_week_date(app, week):
    #gets the previous week, given a week
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
    #gets the next week, given a week
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

