'''
    if not same_day:
        if is_strictly_time_greater(t2_end, "00:15"):
            return False
        else:
            canShiftUp = False
    if move_time == "00:00" or move_time == "0:00":
        canShiftDown = False
    #then check if move time would conflict with current events
    events_overlapped = []
    for i in range(len(days_schedule)):
        #check for overlap with event
        t1_start = days_schedule[i]["start_time"]
        t1_end = days_schedule[i]["end_time"]
        if (times_overlap(t1_start, t1_end, t2_start, t2_end)):
            events_overlapped.append((days_schedule[i], i))
    if events_overlapped == []:
        return None
    #start time of move event is either before or after or on start time of first event overlapped
    if is_time_greater_or_eq(t2_start,events_overlapped[0][0]["start_time"]):
        
        pass
    else:
        pass

    #for i in range(len(events_overlapped)):
        
            #if overlap is 15 minutes or less, can shift the move time up or down 
            
            if is_time_greater_or_eq(t2_start,t1_start): #if overlap at end of event
                duration = find_duration_between(t2_start, t2_end)
                if not is_time_greater_or_eq(duration,"00:15"):
                    same_day, new_t2_start = add_duration_to_time(t2_start, duration)
                    same_day, new_t2_end = add_duration_to_time(new_t2_start, move_duration)
                    if not same_day: 
                        events_overlapped.append(days_schedule[i])
                        continue
                    
                    elif i < len(days_schedule) - 1: #else check if new time conflicts with time after it
                        new_t1_start = days_schedule[i + 1]["start_time"]
                        new_t1_end = days_schedule[i]["end_time"]
                        if times_overlap(new_t1_start, new_t1_end, new_t2_start, new_t2_end):
                            return ()
            if is_time_greater_or_eq(t2_end,t1_start): #if overlap at beginning of event
                duration = find_duration_between(t2_start, t2_end)
                if not is_time_greater_or_eq(duration,"00:15"):
                    same_day, new_time = add_duration_to_time(t2_start, duration)'''
                    
import random 
for i in range(2000):
    x = random.randint(1, 3)
    if x == 3:
        day = random.randint(1, 7)
        if day == 1 or day == 2 or day == 5: #sun, mon, fri 
            if random.randint(0,1) == 0:
                time = 10
            else:
                time = 11
        else:
            time = 3
    elif x == 2:
        day = random.randint(1, 7)
        if day == 3 or day == 5 or day == 6: #tue, fri, sat 
            if random.randint(0,1) == 0:
                time = 5
            else:
                time = 6
        else: 
            time = 12
    else:
        day = random.randint(1, 7)
        if day == 2 or day == 1 or day == 4: #sun, mon, th
            if random.randint(0,1) == 0:
                time = 2
            else:
                time = 4
        else: 
            time = 22

    print(f'{day},{time},{x}')


def merge(a, start1, start2, end):
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and (a[index1] > a[index2]))):
            aux[i] = a[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]

def mergeSort(a):
    n = len(a)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(a, start1, start2, end)
        step *= 2
