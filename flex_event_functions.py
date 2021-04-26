import csv
from event_functions import *
from date_functions import *
import copy

def get_flexible_csv(schedule_folder,eventId):
    #gets the file of the csv file for a specific event and calendar
    file = eventId + ".csv"
    return f'data/{schedule_folder}/flexible_event_records/{file}'

def make_times_list(schedule_folder,eventId):
    #for a given event, makes a list with most optimal to least optimal times
    weights = [1, .75, .5, .25, .12, .6, .3, .2, .1, 0.5]
    weights_past_three = .25
    times_set = {}
    num_days_seen = 0
    weeks_passed = 0
    with open(get_flexible_csv(schedule_folder,eventId), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        entries_num = len(list(csv_file)) - 1
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        for row in reader:
            date_time_list = get_half_hour_between(row["time_started"], row["time_ended"])
            mood = row['mood']
            weekday = row['weekday']
            num_days_seen += 1
            if num_days_seen == 7:
                num_days_seen = 0
                if weeks_passed < len(weights) - 1:
                    weeks_passed += 1
            if date_time_list == None:
                continue
            multiplier = 1
            if row['missed/present'] == 'missed': multiplier = -1
            for t in date_time_list:
                date_time = weekday + ',' + t
                value = weights[weeks_passed]
                if date_time not in times_set:
                    times_set[date_time] = [0, {weeks_passed: [mood]}]
                times_set[date_time][0] = times_set[date_time][0] + value*multiplier
                if weeks_passed in times_set[date_time][1]:
                    times_set[date_time][1][weeks_passed].append(mood)
                else:
                    times_set[date_time][1][weeks_passed] = [mood]
        return times_set

def generate_mood_weights(n):
    weights = [1]
    if n > 1:
        for i in range(1, n):
            weights.append(weights[i - 1])
            past_weight = weights[i - 1]
            weights[i - 1] = past_weight / 2
            weights[i] = past_weight / 2
    return weights

def get_mood_index(times_set):
    new_time_set = {}
    for time in times_set:
        mood_set = times_set[time][1]
        num_weeks = len(mood_set) 
        weights = generate_mood_weights(num_weeks)
        average_mood = 0
        count = 0
        for weeks in mood_set:
            moods_in_week = []
            for m in mood_set[weeks]:
                moods_in_week.append(int(m))
            mood_set[weeks] = [sum(moods_in_week) / len(mood_set[weeks])]
            average_mood += mood_set[weeks][0] * weights[count]
            count += 1
        times_set[time][1] = average_mood
    return times_set

def is_lower_priority(event1, event2):
    #takes in two events
    #returns True if the first input is a lower priority than the second
    if event1[1][0] < event2[1][0]:
        return True
    elif event1[1][0] == event2[1][0] and event1[1][1] < event2[1][1]:
        return True
    else:
        return False

def is_higher_priority(event1, event2):
    #takes in two events
    #returns True if the first input is a lower priority than the second
    if event1[1][0] > event2[1][0]:
        return True
    elif event1[1][0] == event2[1][0] and event1[1][1] > event2[1][1]:
        return True
    else:
        return False

def merge(a, start1, start2, end):
    #sorting algorithm adapted from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and is_lower_priority(a[index1], a[index2]))):
            aux[i] = a[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]

def merge_sort_times(times_list):
    #sorting algorithm adapted from https://www.cs.cmu.edu/~112/notes/notes-efficiency.html#sorting
    sorted_times = []
    n = len(times_list)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(times_list, start1, start2, end)
        step *= 2
    return sorted_times

def sort_times_list(times_set):
    #sorts the times with the most to least priority
    times_list = list(times_set.items())
    merge_sort_times(times_list)
    return times_list

def get_priority_list(schedule_folder,eventId):
    #returns the priority list of a specified event 
    times_set = make_times_list(schedule_folder,eventId)
    times_set = get_mood_index(times_set)
    times_list = sort_times_list(times_set)
    '''print("times", times_list)
    for i in times_list:
        print(i)'''
    return times_list

def get_all_priority_lists(schedule_folder, day):
    #returns the priority list of all the flexible events
    priority_lists = {}
    event_ids = {}
    weekly_durations = {"sun":"", "mon":"", "tue":"", "wed":"", "th":"", "fri":"", "sat":"",}
    with open(get_flex_events_csv(schedule_folder), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                end_date = date.fromisoformat(row['recurring_end'])
                if day <= end_date:
                    priority_lists[row['id']] = get_priority_list(schedule_folder,row['id'])
                    event_ids[row['id']] = {"recurrence_type": row['recurrence_type']}
                    if row['recurrence_type'] == "daily":
                        my_weekly_durations = copy.copy(weekly_durations)
                        for weekday in weekly_durations:
                            my_weekly_durations[weekday] = row['duration']
                            event_ids[row['id']]['duration'] = my_weekly_durations
                    elif row['id'] == "FE-1": #testing purposes
                        num_days = 3
                        durations = {}
                        for i in range(num_days):
                            durations[i] = row['duration']
                        event_ids[row['id']]['duration'] = durations
                    elif row['recurrence_type'] == "weekly":
                        event_ids[row['id']]['duration'] = {row['duration']}
                    event_ids[row['id']]['single_duration'] = row['duration']
            except:
                pass
    return priority_lists, event_ids

def flex_schedule_helper(event_ids, priority_lists, schedule, weekday_dict):
    #recursive function to schedule flexible events based on priority
    #returns the new schedule
    #need to finish
    if check_schedule_done(event_ids):
        return schedule
    else:
        for ids in priority_lists:
            move = priority_lists[ids][0]
            valid = isValidMove(ids, event_ids[ids], move, schedule, weekday_dict)
            #print(weekday_dict)
            break
        return None

def check_schedule_done(event_ids):
    #checks if the schedule is finished
    for ids in event_ids:
        if event_ids[ids]["recurrence_type"] == "daily" or ids == "FE-1":
            for day in event_ids[ids]["duration"]:
                if event_ids[ids]["duration"][day] != 0 and event_ids[ids]["duration"][day] != "0:00":
                    return False
        elif event_ids[ids]["recurrence_type"] == "weekly":
            if event_ids[ids]["duration"] != 0 and event_ids[ids]["duration"] != "0:00":
                return False
    return True

def isValidMove(id, event_info, move, schedule, weekday_dict):
    #checks if the time is a valid time to schedule the event
    move_duration = event_info['single_duration']
    move_weekday, move_time = move[0].split(',')
    move_time_start = move_time
    move_time_end = duration_time_time(move_time_start, move_duration)
    if move_time_end[0] == False:
        return False
    move_time_end = move_time_end[1]
    if event_info["recurrence_type"] == "daily" and event_info["duration"][move_weekday] == 0:
        return False
    elif id == "FE-1":
        for days in event_info["duration"]:
            if event_info["duration"][days] == 0:
                return False
    elif event_info["recurrence_type"] == "weekly":
        if event_info["duration"] == 0:
            return False
    for events in schedule:
        if weekday_dict[events['date']] == move_weekday:
            if times_overlap(events['start_time'], events['end_time'], 
            move_time_start, move_time_end):
                pass
    return True
         
def generate_flexible_schedule(schedule_folder, strict_schedule, week):
    #generates the schedule of flexible events
    priority_lists, events_ids = get_all_priority_lists(schedule_folder, get_current_date())
    """ i in priority_lists:
        print(i, priority_lists[i])"""
    print(events_ids)
    strict_schedule = copy.deepcopy(strict_schedule)
    weekday_dict = get_day_to_weekday_dict(week)
    flexible_schedule = flex_schedule_helper(events_ids, priority_lists, strict_schedule, weekday_dict)
    #return priority_lists

#print(generate_flexible_schedule('sample_schedule1'))
