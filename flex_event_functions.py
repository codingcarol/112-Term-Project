import csv
from event_functions import *
from date_functions import *
import copy


def get_flexible_csv(schedule_folder,event_id):
    #gets the file of the csv file for a specific event and calendar
    file = event_id + ".csv"
    return f'data/{schedule_folder}/flexible_event_records/{file}'

def get_event_weight(num_entries, current_week):
    #gets the weight for the value, given the week
    num_weeks_entered = num_entries // 7
    remainder_days = num_entries % 7
    is_remainder = False
    if remainder_days > 0: is_remainder = True
    if is_remainder: 
        num_weeks_entered += 1
    if current_week == 1 or current_week == 0:
        return 1
    elif current_week == 2:
        return .75
    elif current_week == 3:
        return .5
    else:
        starting_weight = .5
        for i in range(current_week - 3):
            starting_weight /= 2
        return starting_weight

def make_times_list(schedule_folder, event_id, event_duration):
    #for a given event, makes a list with most optimal to least optimal starting times
    times_set = {}
    num_days_seen = 0
    weeks_passed = 0
    remainder = True
    with open(get_flexible_csv(schedule_folder,event_id), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        entries_num = len(list(csv_file)) - 1
        week = entries_num // 7
        remainder_days = entries_num % 7 
        if remainder_days != 0:
            week += 1
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        for row in reader:
            t = row["time_started"]
            mood = row['mood']
            weekday = row['weekday']
            num_days_seen += 1
            if remainder and num_days_seen == remainder_days:
                num_days_seen = 0
                week -= 1
                remainder = False
            elif num_days_seen == 7 and week > 1: #to determine the weight of each entry
                num_days_seen = 0
                week -= 1 
            multiplier = 1
            if row['missed/present'] == 'missed': multiplier = -1
            date_time = weekday + ',' + t
            value = get_event_weight(entries_num, week)
            if date_time not in times_set:
                times_set[date_time] = [0, {week: [mood]}]
            times_set[date_time][0] = times_set[date_time][0] + value*multiplier
            if week in times_set[date_time][1]:
                times_set[date_time][1][week].append(mood)
            else:
                times_set[date_time][1][week] = [mood]
        return times_set

def generate_mood_weights(n):
    #generates the weights of the moods
    weights = [1]
    if n > 1:
        for i in range(1, n):
            weights.append(weights[i - 1])
            past_weight = weights[i - 1]
            weights[i - 1] = past_weight / 2
            weights[i] = past_weight / 2
    return weights

def get_mood_index(times_set):
    #finds the weighted average of the moods
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

def get_priority_list(schedule_folder,event_id,event_duration):
    #returns the priority list of a specified event 
    times_set = make_times_list(schedule_folder,event_id,event_duration)
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
                    priority_lists[row['id']] = get_priority_list(schedule_folder,row['id'],row['duration'])
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
                        event_ids[row['id']]['duration'] = {0: row['duration']}
                    event_ids[row['id']]['single_duration'] = row['duration']
            except:
                pass
    return priority_lists, event_ids

def flex_schedule_helper(event_ids, priority_lists, schedule, weekday_dict):
    if check_schedule_done(event_ids):
        return schedule
    else:
        for e in event_ids:
            for move in priority_lists[e]:
                legal = is_move_legal(move[0], event_ids[e], e, schedule, weekday_dict)
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

def event_is_complete(events_info, weekday):
    #gets the current state of filled events and a given weekday
    #returns true if the day does not have a certain event, returns false if it does not have it
    if events_info["recurrence_type"] == "daily":
        if events_info["duration"][weekday] != 0:
            return False
        return True
    elif events_info["recurrence_type"] == "weekly": 
        open_spot = False
        for spot in events_info["duration"]:
            if spot == weekday:
                return True
            if isinstance(spot, int):
                open_spot = True
        return open_spot

def organize_schedule_by_weekdays(schedule, weekday_dict):
    #creates a schedule of events organized by weekday
    new_schedule = {"sun": [], "mon": [], "tue": [], "wed": [], "th": [], "fri": [], "sat": []}
    for event in schedule:
        event_date = event["date"]
        event_weekday = weekday_dict[event_date]
        new_schedule[event_weekday].append(event)
    return new_schedule

def schedule_conflict_helper(times_list, move_duration, schedule, move_types, last_time):
    #recursive function for finding the scheduling conflicts
    if times_list == [] or (last_time != None and move_types[last_time] == []):
        return (move_types, last_time)
    else:
        t2_start = times_list[0][0]
        move_types[t2_start] = []
        for i in range(len(schedule)):
            t1_start = schedule[i]["start_time"]
            t1_end = schedule[i]["end_time"]
            t2_end = times_list[0][1]
            if (times_overlap(t1_start, t1_end, t2_start, t2_end)):
                move_types[t2_start].append(schedule[i]) 
        return schedule_conflict_helper(times_list[1:], move_duration, schedule, move_types, t2_start)

def get_daily_flex_events(days_schedule):
    #gets the flexible events of a given daily schedule
    flex_events = dict()
    for e in days_schedule:
        if "FE" in e['id']:
            flex_events[e['id']] = (e['start_time'], e['end_time'])
    return flex_events 

def schedule_conflict_type(move_day, move_time, move_duration, schedule):
    #determines if there is a scheduling conflict between the move and the schedule
    days_schedule = schedule[move_day]
    times_list = get_times_within_fifteen_min(move_time)
    accurate_times = []
    for times in times_list:
        same_day, new_time = add_duration_to_time(times, move_duration)
        if same_day:
            accurate_times.append((times, new_time))
    if accurate_times == []: return ("strict", None)
    conflicts, last_time = schedule_conflict_helper(accurate_times, move_duration, days_schedule, {}, None)
    if conflicts[last_time] == []:
        return (None, last_time)
    else:
        days_flex_events = get_daily_flex_events(days_schedule)
        flexible_conflicts = dict()
        seen_conflicts = set()
        for t in conflicts:
            all_flexible = True
            flexibles = []
            for event_conflict in conflicts[t]:
                if 'SE' in event_conflict['id'] or 'RE' in event_conflict['id']:
                    all_flexible = False
                    break
                elif 'FE' in event_conflict['id']:
                    flexibles.append(event_conflict['id'])
            if all_flexible:
                flexibles = tuple(flexibles)
                t1_start = days_flex_events[flexibles[0]][0]
                t1_end = days_flex_events[flexibles[0]][1]
                t2_start = t
                same_day, t2_end = add_duration_to_time(t, move_duration)
                overlap_time = get_overlap_time(t1_start, t1_end, t2_start, t2_end)
                if flexibles in seen_conflicts:
                    #choose conflicting time with the most overlap for first event
                    current_value_overlap = flexible_conflicts[flexibles][1]
                    if is_strictly_time_greater(overlap_time, current_value_overlap):
                        flexible_conflicts[flexibles] = t, overlap_time
                else:
                    seen_conflicts.add(flexibles)
                    flexible_conflicts[flexibles] = t, overlap_time
        if len(flexible_conflicts) > 0:
            return ("flex", flexible_conflicts)
        else:
            return ("strict", None)

def better_flexible_event(new_move, new_duration, current_flexible_events):
    pass

def is_move_legal(move, events_info, event_id, schedule, weekday_dict):
    #checks if the given move is legal 
    move_day, move_time = move.split(",")[0], move.split(",")[1]
    move_duration = events_info["single_duration"]
    if event_is_complete(events_info, move_day):
        return False
    conflict_type, last_time = schedule_conflict_type(move_day, move_time, move_duration, schedule)
    print(conflict_type, last_time)
    if conflict_type == None:
        return True
    elif conflict_type == "strict":
        return False
    elif conflict_type == "flex":
        return ""

def generate_flexible_schedule(schedule_folder, strict_schedule, week):
    #generates the schedule of flexible events
    priority_lists, event_ids = get_all_priority_lists(schedule_folder, get_current_date())
    weekday_dict = get_day_to_weekday_dict(week)
    strict_schedule = copy.deepcopy(strict_schedule)
    for i in priority_lists:
        print(i, priority_lists[i])
    new_strict_schedule = organize_schedule_by_weekdays(strict_schedule, weekday_dict)
    flexible_schedule = flex_schedule_helper(event_ids, priority_lists, new_strict_schedule, weekday_dict)
    #return priority_lists
