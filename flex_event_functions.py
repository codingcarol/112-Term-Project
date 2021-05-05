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
            #keep track of days and weeks that have passed 
            num_days_seen += 1
            if remainder and num_days_seen == remainder_days:
                num_days_seen = 0
                week -= 1
                remainder = False
            elif num_days_seen == 7 and week > 1: #to determine the weight of each entry
                num_days_seen = 0
                week -= 1 
            multiplier = 1
            if row['missed/present'] == 'missed': multiplier = -1 #if it is a missed event, negative
            date_time = weekday + ',' + t
            value = get_event_weight(entries_num, week) #gets the weight
            if date_time not in times_set: #if a new time, make a new item in set
                times_set[date_time] = [0, {week: [mood]}] 
                #format is: time: [time_score, list of weekly moods]
            #adds the weighted value to the current time score
            times_set[date_time][0] = times_set[date_time][0] + value*multiplier
            if week in times_set[date_time][1]: #add mood according to the week number
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
    return times_list

def get_all_priority_lists(schedule_folder, day):
    #returns the priority list of all the flexible events
    priority_lists = {} #for each flexible event, get all the priority times for that event
    event_ids = {} #for each flexible event, keeps track of other data like title, recurrence type
    weekly_durations = {"sun":"", "mon":"", "tue":"", "wed":"", "th":"", "fri":"", "sat":"",}
    with open(get_flex_events_csv(schedule_folder), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        reader = csv.DictReader(csv_file)
        for row in reader: 
            try:
                end_date = date.fromisoformat(row['recurring_end'])
                if day <= end_date:
                    priority_lists[row['id']] = get_priority_list(schedule_folder,row['id'],row['duration'])
                    #^adds priority list
                    #rest of loop adds other info to event_id dict 
                    event_ids[row['id']] = {"recurrence_type": row['recurrence_type']}
                    event_ids[row['id']]['title'] = row['title']
                    event_ids[row['id']]['description'] = row['description']
                    if row['recurrence_type'] == "daily":
                        my_weekly_durations = copy.copy(weekly_durations)
                        for weekday in weekly_durations:
                            my_weekly_durations[weekday] = row['duration']
                            event_ids[row['id']]['duration'] = my_weekly_durations
                    elif row['recurrence_type'] == "some":
                        num_days = int(row['num_days'])
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

def get_positive_priority_list(priority_lists):
    #gets the priority list with positive values, gets only prioritized/favored times
    positive_priority_list = {}
    for event in priority_lists:
        positive_priority_list[event] = []
        for move in priority_lists[event]:
            if move[1][0] > 0:
                positive_priority_list[event].append(move)
    return positive_priority_list

def event_is_complete(events_info, weekday):
    #gets the current state of filled events and a given weekday
    #returns true if the day does not have a certain event, returns false if it does not have it
    if events_info["recurrence_type"] == "daily":
        if events_info["duration"][weekday] != 0:
            return False
        return True
    elif events_info["recurrence_type"] == "weekly": 
        open_spot = True
        for spot in events_info["duration"]:
            if spot == weekday:
                return True
            if isinstance(spot, int):
                open_spot = False
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
    #recursive function for finding the scheduling conflicts, returns a list of all conflicts for each time
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
    for times in times_list: #tests all the times within fifteen minutes of the priority time, makes a list of these times
        same_day, new_time = add_duration_to_time(times, move_duration)
        if same_day:
            accurate_times.append((times, new_time))
    if accurate_times == []: return ("strict", None)
    conflicts, last_time = schedule_conflict_helper(accurate_times, move_duration, days_schedule, {}, None)
    #^checks if there is a scheduling conflict with any of the possible times
    if conflicts[last_time] == []: #if there are no conflict for a certain time, return None and the last time
        return (None, last_time)
    else: #figures out of there are any times that just conflict with just one flexible event
        #if so, return the flexible event. else, say there are only strict 
        days_flex_events = get_daily_flex_events(days_schedule)
        flexible_conflicts = dict() #keeps track of time and the event is conflicts with 
        seen_conflicts = set()
        for t in conflicts: #find all the times where there are only flexible event conflicts
            all_flexible = True
            flexibles = []
            for event_conflict in conflicts[t]:
                if 'SE' in event_conflict['id'] or 'RE' in event_conflict['id']:
                    all_flexible = False
                    break
                elif 'FE' in event_conflict['id']:
                    flexibles.append((event_conflict['id'], event_conflict['start_time']))
            if all_flexible:
                flexibles = tuple(flexibles)
                t1_start = days_flex_events[flexibles[0][0]][0]
                t1_end = days_flex_events[flexibles[0][0]][1]
                t2_start = t
                same_day, t2_end = add_duration_to_time(t, move_duration)
                overlap_time = get_overlap_time(t1_start, t1_end, t2_start, t2_end)
                if flexibles in seen_conflicts:
                    #if conflict already week, choose conflicting time with the most overlap for first event
                    current_value_overlap = flexible_conflicts[flexibles]['overlap']
                    if is_strictly_time_greater(overlap_time, current_value_overlap):
                        flexible_conflicts[flexibles]['start_t'] = t
                        flexible_conflicts[flexibles]['end_t'] = t2_end
                        flexible_conflicts[flexibles]['overlap'] = overlap_time
                else:
                    seen_conflicts.add(flexibles)
                    flexible_conflicts[flexibles] = dict()
                    flexible_conflicts[flexibles]['start_t'] = t
                    flexible_conflicts[flexibles]['end_t'] = t2_end
                    flexible_conflicts[flexibles]['overlap'] = overlap_time
        single_conflicts = {}
        for k in flexible_conflicts:
            if len(k) <= 1:
                single_conflicts[k[0][0]] = flexible_conflicts[k]
                single_conflicts[k[0][0]]['fe_time'] = k[0][1]
        if len(single_conflicts) > 0: #returns time and the vent that it conflicts with
            return ("flex", single_conflicts)
        else:
            return ("strict", None)

def find_longest_event(all_events, event_ids, e_id):
    #find the longest event in a list of events
    durations = dict() #get determine if one has as significantly longer duration 
    for events in all_events:
        if events in event_ids.keys():
            t = event_ids[events]["single_duration"]
            if t in durations:
                if events == e_id:
                    durations[t].insert(0, events)
                durations[t].append(events)
            else:
                durations[t] = [events]
    longest = []
    longest_time = 0
    for t in durations: #consider an event longer only if time is 1.5 hours more than current longest
        minutes = get_duration_as_int(t)
        if minutes >= longest_time + 90 or longest_time == 0:
            longest_time = minutes
            longest = []
            for ids in durations[t]:
                longest.append(ids)
        elif minutes <= longest_time + 60 and minutes >= longest_time - 60:
            for ids in durations[t]:
                longest.append(ids)
    return longest

def find_needs_most_occurance(all_events, event_ids, e_id):
    #find events with the most upcoming occurances needed in the week
    needed_occurances = {}
    for events in all_events:
        occurances = 0
        for k in event_ids[events]["duration"]:
            if event_ids[events]["duration"][k] != 0:
                occurances += 1
        if occurances in needed_occurances:
            if events == e_id:
                needed_occurances[occurances].insert(0, events)
            needed_occurances[occurances].append(events)
        else:
            needed_occurances[occurances] = [events]
    return needed_occurances

def least_flexible_events(e_id, event_ids, current_flexible_e, priority_lists):
    #finds the least flexible event
    all_events = {e_id} #get all the events considering
    least_to_most_flex = []
    for key in current_flexible_e:
        if key in event_ids:
            all_events.add(key)
    longest = find_longest_event(all_events, event_ids, e_id) #determines the longest event
    if len(longest) == 1: #if one is significantly longer, add it to the list
        least_to_most_flex.append(longest[0])
        all_events.remove(longest[0])
    most_needed = find_needs_most_occurance(all_events, event_ids, e_id) #find event with most occurance
    for keys in reversed(sorted(most_needed.keys())):
        for e in most_needed[keys]:
            least_to_most_flex.append(e)
    return least_to_most_flex #returns a list of events from the least to most flexible 

def is_move_legal(move, events_info, event_id, schedule, weekday_dict, priority_lists):
    #checks if the given move is legal 
    move_day, move_time = move.split(",")[0], move.split(",")[1]
    move_duration = events_info["single_duration"]
    if event_is_complete(events_info, move_day):
        return (False,)
    conflict_type, last_time = schedule_conflict_type(move_day, move_time, move_duration, schedule)
    if conflict_type == None: #no conflict
        return (True, (move_day, last_time))
    elif conflict_type == "strict": #not legal, conflict with strict event
        return (False,)
    elif conflict_type == "flex": #flexible, conflicts with flexible event
        return ("flex", last_time)

def check_done(priority_indexes, priority_lists):
    #checks if all events are placed
    for e in priority_indexes:
        if priority_indexes[e] < len(priority_lists[e]):
            return False
    return True 

def get_date_from_weekday_dict(weekday_dict, weekday):
    #gets date from a given weekday
    for key in weekday_dict:
        if weekday_dict[key] == weekday:
            return key

def add_move_to_schedule(event_ids, move, schedule, e, weekday_dict):
    #places the new event in the schedule
    weekday = move[0]
    t = move[1]
    new_event = {'id': e, 'title': event_ids[e]['title'], 'date': get_date_from_weekday_dict(weekday_dict, weekday),
    'start_time': t, 'end_time': add_duration_to_time(t, event_ids[e]['single_duration'])[1],
    'description': event_ids[e]['description']}
    for i in range(len(schedule[weekday])):
        if is_strictly_time_greater(schedule[weekday][i]['start_time'], new_event['start_time']):
            schedule[weekday].insert(i, new_event)
            return i
            break
        elif i == len(schedule[weekday]) - 1:
            schedule[weekday].append(new_event)
            return i + 1

def remove_move_from_schedule(insert_index, schedule, adjusted_move):
    #removes event from schedule
    weekday = adjusted_move[0]
    schedule[weekday].pop(insert_index)

def place_event_in_tracker(event_ids, move, e):
    #notes in the event tracker that a day has been placed for a certain event
    day = move[0]
    if event_ids[e]["recurrence_type"] == "daily":
        event_ids[e]["duration"][day] = 0
    else:
        for n in event_ids[e]["duration"]:
            if isinstance(n, int):
                del event_ids[e]["duration"][n]
                event_ids[e]["duration"][day] = 0
                break

def remove_move_from_tracker(event_ids, move, e):
    #removes event from the event tracker
    day = move[0]
    event_ids[e]["duration"][day] = event_ids[e]["single_duration"]

def flex_schedule_helper(event_ids, priority_lists, schedule, weekday_dict, priority_indexes):
    #fill the highest priority slots if possible
    if check_done(priority_indexes, priority_lists):
        return ('schedule', schedule)
    else:
        for e in event_ids: #iterate through each event
            for move in priority_lists[e][priority_indexes[e]:]: #iterate through each priority move
                legal = is_move_legal(move[0], event_ids[e], e, schedule, weekday_dict, priority_lists)
                #check if legal
                if isinstance(legal, tuple) and legal[0] == True: #if legal
                    adjusted_move = legal[1]
                    place_event_in_tracker(event_ids, adjusted_move, e) #place move in event tracker
                    insert_index = add_move_to_schedule(event_ids, adjusted_move, schedule, e, weekday_dict) #add event to schedule
                    current_index = copy.copy(priority_indexes)
                    priority_indexes[e] += 1
                    sol = flex_schedule_helper(event_ids, priority_lists, schedule, weekday_dict, priority_indexes) #recurse
                    #two options - backtrack or found the answer
                    if sol == None or sol[0] == "schedule":
                        return sol
                    elif sol[0] == 'replace' and sol[1] == e and sol[2]['fe_time'] == adjusted_move[1]:
                        #at move that was replaced before, undo it and stop backtracking and move forward again
                        priority_indexes = current_index
                        remove_move_from_schedule(insert_index, schedule, adjusted_move)
                        remove_move_from_tracker(event_ids, adjusted_move, e) 
                        continue
                    elif sol[0] == 'replace':
                        #if we are backtracking, undo the event
                        priority_indexes = current_index
                        remove_move_from_schedule(insert_index, schedule, adjusted_move)
                        remove_move_from_tracker(event_ids, adjusted_move, e) 
                        return sol
                elif isinstance(legal, tuple) and legal[0] == False: #do not place move if not legal
                    priority_indexes[e] += 1
                    if check_done(priority_indexes, priority_lists):
                        return ('schedule', schedule)
                else: #does this is flexible
                    least_flexibles = least_flexible_events(e, event_ids, legal[1], priority_lists)
                    if least_flexibles[0] != e: #keeps going if the event is not legal/wont replace flexible
                        priority_indexes[e] += 1
                    else: #event replaces a flexible event so backtrack
                        replaced_val = least_flexibles[-1]
                        return ('replace', replaced_val, legal[1][replaced_val])
        return None

def check_schedule_done(event_ids):
    #checks if the schedule is finished
    for ids in event_ids:
        for day in event_ids[ids]["duration"]:
            if event_ids[ids]["duration"][day] != 0:
                return False
    return True

def find_moves_of_day(flexible_schedule, given_day, event_duration):
    #finds the open moves for an event of the given day in a schedule
    #basically returns a list of open time slots 
    open_moves = []
    if given_day != None:
        if (given_day in flexible_schedule and len(flexible_schedule[given_day]) > 0 and
        flexible_schedule[given_day][0]["start_time"] != "00:00"):
            start_t = "00:00"
            end_t = flexible_schedule[given_day][0]["start_time"]
            duration =  find_duration_between("00:00", end_t)
            if is_time_greater_or_eq(duration,event_duration):
                open_moves.append({'start_time': start_t, 
                'end_time': end_t, 'duration': duration})
        for i in range(len(flexible_schedule[given_day]) - 1):
            start_t = flexible_schedule[given_day][i]["end_time"]
            end_t = flexible_schedule[given_day][i + 1]["start_time"]
            duration =  find_duration_between(start_t, end_t)
            if is_time_greater_or_eq(duration,event_duration):
                open_moves.append({'start_time': start_t, 
                'end_time': end_t, 'duration': duration})
        if (given_day in flexible_schedule and len(flexible_schedule[given_day]) > 0 and
        flexible_schedule[given_day][-1]["end_time"] != "11:59"):
            start_t = flexible_schedule[given_day][-1]["end_time"]
            end_t = "11:59"
            duration =  find_duration_between(start_t, end_t)
            if is_time_greater_or_eq(duration,event_duration):
                open_moves.append({'start_time': start_t, 
                'end_time': end_t, 'duration': duration})
    return open_moves

def make_event_zero(event_ids, move, e):
    #undos an event, shows that a event that was placed in a certain day is not placed there anymore
    day = move[0]
    if event_ids[e]["recurrence_type"] == "daily":
        event_ids[e]["duration"][day] = 0
    else:
        for n in event_ids[e]["duration"]:
            if event_ids[e]["duration"][n] != 0:
                event_ids[e]["duration"][n] = 0
                break

def get_open_moves(event_ids, flexible_schedule, given_day, event_duration):
    #gets the open moves of each day for an event
    count = 0
    for i in event_ids["duration"]:
        if event_ids["duration"][i] != 0:
            count += 1
    if count == 0: return []
    open_moves = {}
    if given_day != None:
        if event_ids["duration"][given_day] == 0: 
            return {}
        open_moves[given_day] = find_moves_of_day(flexible_schedule, given_day, event_duration)
        return open_moves
    for day in flexible_schedule:
        if day in event_ids["duration"] and event_ids["duration"][day] == 0: continue
        if "taken" in event_ids and day in event_ids["taken"]: continue
        open_moves[day] = find_moves_of_day(flexible_schedule, day, event_duration)
    return open_moves

def remove_move_from_scheduled(schedule, adjusted_move, d, e):
    #removes event from schedule
    for i in range(len(schedule[d])):
        if e == schedule[d][i]['id']:
            break
    schedule[d].pop(i)
    return

def fill_empty_spots(event_ids, flexible_schedule, weekday_dict):
    #place the events that still need to be placed
    if check_schedule_done(event_ids):
        return flexible_schedule
    for e in event_ids:
        for d in event_ids[e]["duration"]:
            day = None
            if event_ids[e]["recurrence_type"] == "daily":
                day = d
            moves = get_open_moves(event_ids[e], flexible_schedule, day, event_ids[e]["single_duration"])
            for new_day in moves:
                for m in moves[new_day]:
                    move = (new_day, m['start_time'])
                    add_move_to_schedule(event_ids, move, flexible_schedule, e, weekday_dict)
                    make_event_zero(event_ids, move, e) 
                    if "taken" not in event_ids[e]:
                        event_ids[e]["taken"] = {new_day}
                    else: event_ids[e]["taken"].add(new_day)
                    sol = fill_empty_spots(event_ids, flexible_schedule, weekday_dict)
                    if sol != None:
                        return flexible_schedule
                    remove_move_from_scheduled(flexible_schedule, move, new_day, e)
                    remove_move_from_tracker(event_ids, move, e) 
    return None

def merge_days(flexible_schedule):
    #merges the flexible schedule dict into a list of events
    total_schedule = []
    for d in flexible_schedule:
        for e in flexible_schedule[d]:
            total_schedule.append(e)
    return total_schedule

def generate_flexible_schedule(schedule_folder, strict_schedule, week):
    #generates the schedule of flexible events
    priority_lists, event_ids = get_all_priority_lists(schedule_folder, get_current_date())
    weekday_dict = get_day_to_weekday_dict(week)
    strict_schedule = copy.deepcopy(strict_schedule)
    positive_priority_lists = get_positive_priority_list(priority_lists)
    priority_indexes = {}
    for e in event_ids:
        priority_indexes[e] = 0
    schedule = organize_schedule_by_weekdays(strict_schedule, weekday_dict)
    try:
        schedule = flex_schedule_helper(event_ids, positive_priority_lists, schedule, weekday_dict, priority_indexes)[1]
    except:
        pass
    schedule = fill_empty_spots(event_ids, schedule, weekday_dict)
    merged_schedule = merge_days(copy.deepcopy(schedule))
    return merged_schedule
