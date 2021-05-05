from inputBox import *
import string 
from create_event_draw import *
from typing import *
from date_functions import *
from event_functions import *
import csv
import os
from flex_event_functions import organize_schedule_by_weekdays

def createEvent_keyPressed(app, event):
    #behavior when key is pressed
    if app.typing and (type(app.text_box) == TextBox or type(app.text_box) == NumTextBox):
        #typing event
        typing_event(app, event)
        return
    if event.key == "Escape":
        app.schedule = construct_strict_schedule(app)
        app.mode = "calendarHome"

def createEvent_mousePressed(app, event):
    #behavior when mouse is pressed
    reset_typing_setting(app)
    item = get_clicked_item(app, event.x, event.y)
    if type(item) == RectButton: #choose button
        app.recentBtn = item.name
        if item.name == "Strict":
            SE_btn(app)
        if item.name == "Recurring Strict":
            RE_btn(app)
        if item.name == "Flexible":
            FE_btn(app)
        if item.name in ['sun', 'mon', 'tue', 'wed', 'th', 'fri', 'sat']:
            if item.get_value() in ['sun', 'mon', 'tue', 'wed', 'th', 'fri', 'sat']:
                item.set_value("")
                item.set_fill("#dee1ff")
            else:
                item.set_value(item.name)
                item.set_fill("#d6d6d6")
        if item.name == "Save":
            save_btn(app)
    elif type(item) == TextBox or type(item) == NumTextBox:
        #start typing event
        app.typing = True
        app.text_box = item

def createEvent_sizeChanged(app):
    #changes screen size
    change_screen_size(app)

def test_space_available(app, year, month, day, d, t2_start, t2_end):
    #makes sure strict event is not already filled
    old_week = app.currentWeek
    week = get_week(app, year, month, day)
    app.currentWeek = week
    schedule = construct_strict_schedule(app)
    for i in range(len(schedule)):
        if schedule[i]['date'] == d.isoformat():
            t1_start = schedule[i]["start_time"]
            t1_end = schedule[i]["end_time"]
            if (times_overlap(t1_start, t1_end, t2_start, t2_end)):
                app.currentWeek = old_week
                return False
    app.currentWeek = old_week
    return True

def SE_btn(app):
    #when SE button clicked, change the options
    app.current_event_panel = "SE"
    change_to_SE_layout(app)

def change_to_SE_layout(app):
    #updates options for SE 
    for btn in app.SE_btns:
        app.SE_btns[btn].set_coord(SE_layout_manager(app, btn))

def handle_SE_save(app):
    #save SE options and uploads to spreadsheet
    #gets all the values of buttons
    year = app.SE_btns["Year"].get_value()
    month = app.SE_btns["Month"].get_value()
    day = app.SE_btns["Day"].get_value()
    start_t_h = app.SE_btns["Start_H"].get_value()
    start_t_m = app.SE_btns["Start_M"].get_value()
    end_t_h = app.SE_btns['End_H'].get_value()
    end_t_m = app.SE_btns['End_M'].get_value()
    start_time = make_into_time_str(start_t_h, start_t_m)
    end_time = make_into_time_str(end_t_h, end_t_m)
    title = app.event_always_btns['title'].get_value()
    description = app.event_always_btns['description'].get_value()
    #validates the given inputs
    d = nearest_valid_date(app, year, month, day)
    if not test_space_available(app, d.year, d.month, d.day, d, start_time, end_time):
        return
    if (not time_is_valid(start_t_h, start_t_m) or not time_is_valid(end_t_h, end_t_m)
    or not is_strictly_time_greater(end_time, start_time)):
        return  
    #uploads to spreadsheet
    e_id = "SE-"
    with open(get_strict_events_csv(app.schedule_folder), 'r', newline='') as csvfile:
        e_id += str(len(list(csvfile)) + 3)
    with open(get_strict_events_csv(app.schedule_folder), 'a', newline='') as csvfile:
        #headers = ['id','title','date','start_time','end_time','description']
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([e_id,title,d.isoformat(),start_time,end_time,description])

def FE_btn(app):
    #changes options buttons to the flexible event ones
    app.current_event_panel = "FE"
    change_to_FE_layout(app)

def change_to_FE_layout(app):
    #changes the options buttons to flexible event ones
    for btn in app.FE_btns:
        if btn not in ["Num_Days", "Start_H", "Start_M"]:
            app.FE_btns[btn].set_coord(RE_and_FE_layout_manager(app, btn))
        else:
            app.FE_btns[btn].set_coord(FE_layout_manager(app, btn))

def handle_FE_save(app):
    #saves inputs and uploads to flexible event spreadsheet
    #gets the inputs
    year1 = app.FE_btns["Year1"].get_value()
    month1 = app.FE_btns["Month1"].get_value()
    day1 = app.FE_btns["Day1"].get_value()
    year2 = app.FE_btns["Year2"].get_value()
    month2 = app.FE_btns["Month2"].get_value()
    day2 = app.FE_btns["Day2"].get_value()
    start_t_h = app.FE_btns["Start_H"].get_value()
    start_t_m = app.FE_btns["Start_M"].get_value()
    num_days = int(app.FE_btns["Num_Days"].get_value())
    start_time = make_into_time_str(start_t_h, start_t_m)
    title = app.event_always_btns['title'].get_value()
    description = app.event_always_btns['description'].get_value()
    #validates the inputs
    d1 = nearest_valid_date(app, year1, month1, day1)
    d2 = nearest_valid_date(app, year2, month2, day2)
    if not time_is_valid(start_t_h, start_t_m):
        return 
    if num_days <= 0 or num_days > 7:
        return
    if num_days == 1:
        r_type = "weekly"
    elif num_days == 7:
        r_type = "daily"
    else:
        r_type = "some"
    #uploads the new event
    e_id = "FE-"
    with open(get_flex_events_csv(app.schedule_folder), 'r', newline='') as csvfile:
        length = len(list(csvfile))
        e_id += str(length + 5)
    with open(get_flex_events_csv(app.schedule_folder), 'a', newline='') as csvfile:
        #id,title,recurring_start,recurring_end,duration,recurrence_type,num_days,description
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([e_id,title,d1.isoformat(),d2.isoformat(),start_time,r_type,num_days,description])
    path = os.getcwd() + f'/data/{app.schedule_folder}/flexible_event_records'
    #learned to use getcwd from https://linuxize.com/post/python-get-change-current-working-directory/
    with open(os.path.join(path, f'{e_id}.csv'), 'w') as csvfile:
        #used code to make file from https://www.geeksforgeeks.org/create-an-empty-file-using-python/
        writer = csv.writer(csvfile)
        writer.writerow(['date','weekday','time_started','time_ended','missed/present','mood'])

def RE_btn(app):
    #changes options to the RE buttons
    app.current_event_panel = "RE"
    change_to_RE_layout(app)
 
def change_to_RE_layout(app):
    #changes options to the RE buttons
    for btn in app.RE_btns:
        if btn != "Week_Days":
            app.RE_btns[btn].set_coord(RE_and_FE_layout_manager(app, btn))
    app.RE_btns["Week_Days"]["sun"].set_coord(RE_layout_manager(app, "sun"))
    app.RE_btns["Week_Days"]["mon"].set_coord(RE_layout_manager(app, "mon"))
    app.RE_btns["Week_Days"]["tue"].set_coord(RE_layout_manager(app, "tue"))
    app.RE_btns["Week_Days"]["wed"].set_coord(RE_layout_manager(app, "wed"))
    app.RE_btns["Week_Days"]["th"].set_coord(RE_layout_manager(app, "th"))
    app.RE_btns["Week_Days"]["fri"].set_coord(RE_layout_manager(app, "fri"))
    app.RE_btns["Week_Days"]["sat"].set_coord(RE_layout_manager(app, "sat"))
    for btn in app.RE_btns["Week_Days"]:
        app.RE_btns["Week_Days"][btn].set_fill('#d6d6d6')

def handle_RE_save(app):
    #gets inputs and uploads to RE file
    #gets inputs
    year1 = app.RE_btns["Year1"].get_value()
    month1 = app.RE_btns["Month1"].get_value()
    day1 = app.RE_btns["Day1"].get_value()
    year2 = app.RE_btns["Year2"].get_value()
    month2 = app.RE_btns["Month2"].get_value()
    day2 = app.RE_btns["Day2"].get_value()
    start_t_h = app.RE_btns["Start_H"].get_value()
    start_t_m = app.RE_btns["Start_M"].get_value()
    end_t_h = app.RE_btns['End_H'].get_value()
    end_t_m = app.RE_btns['End_M'].get_value()
    start_time = make_into_time_str(start_t_h, start_t_m)
    end_time = make_into_time_str(end_t_h, end_t_m)
    title = app.event_always_btns['title'].get_value()
    description = app.event_always_btns['description'].get_value()
    #validates inputs
    d1 = nearest_valid_date(app, year1, month1, day1)
    d2 = nearest_valid_date(app, year2, month2, day2)
    if (not time_is_valid(start_t_h, start_t_m) or not time_is_valid(end_t_h, end_t_m) or
    not is_strictly_time_greater(end_time, start_time)):
        return  
    count = 0
    valid_days = ""
    for days in app.RE_btns['Week_Days']:
        val = app.RE_btns['Week_Days'][days].get_value()
        if val == "":
            count += 1
            if count == 1:
                valid_days = days[0].upper() + days[1:]
            else:
                valid_days = valid_days + "-" + days[0].upper() + days[1:]
    if count == 1:
        r_type = "weekly"
    elif count == 7:
        r_type = 'daily'
        valid_days = "N/A"
    elif count == 0:
        return
    else:
        r_type = "weekly"
    #uploads events
    e_id = "RE-"
    with open(get_recurring_events_csv(app.schedule_folder), 'r', newline='') as csvfile:
        length = len(list(csvfile))
        e_id += str(length + 5)
    with open(get_recurring_events_csv(app.schedule_folder), 'a', newline='') as csvfile:
        #id,title,recurring_start,recurring_end,exceptions,start_time,end_time,recurrence_type,recurrence_time,description
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([e_id,title,d1.isoformat(),d2.isoformat(),'',start_time,end_time,r_type,valid_days,description])

def save_btn(app):
    #controls which type of event is being saved 
    if app.current_event_panel == "SE":
        handle_SE_save(app)
    elif app.current_event_panel == "FE":
        handle_FE_save(app)
    elif app.current_event_panel == "RE":
        handle_RE_save(app)

def create_event_input(app):
    #creates all the event buttons
    #make all the buttons that are always present
    app.event_always_btns['title'] = TextBox(app.event_title[0], app.event_title[1],
    create_event_layout_manager(app, 'title'), string.printable)
    app.event_always_btns['description'] = TextBox(app.event_description[0], 
    app.event_description[1], create_event_layout_manager(app, 'description'), 
    string.printable)
    app.event_always_btns['SE'] = RectButton(app.event_types_btns[0][0], 
    app.event_types_btns[0][1], 'Strict Events', selector_panel_layout_manager(app, "SE"))
    app.event_always_btns['RE'] = RectButton(app.event_types_btns[1][0], 
    app.event_types_btns[1][1], 'Recurring Events', selector_panel_layout_manager(app, "RE"))
    app.event_always_btns['FE'] = RectButton(app.event_types_btns[2][0], 
    app.event_types_btns[2][1], 'Flexible Events', selector_panel_layout_manager(app, "FE"))
    app.event_always_btns['save'] = RectButton(app.event_save_btn[0], 
    app.event_save_btn[1], 'Save', save_layout_manager(app, "save"))
    #options buttons, make buttons that sometimes change
    year1 = NumTextBox(app.event_date1[0][0],
    app.event_date1[0][1], SE_layout_manager(app, "Year"))
    month1 = NumTextBox(app.event_date1[1][0],
    app.event_date1[1][1], SE_layout_manager(app, "Month"))
    day1 = NumTextBox(app.event_date1[2][0],
    app.event_date1[2][1], SE_layout_manager(app, "Day"))
    start_time_h = NumTextBox(app.event_start_t_h[0], 
    "0", SE_layout_manager(app, "Start_H"))
    end_time_h = NumTextBox(app.event_end_t_h[0],
    "1", SE_layout_manager(app, "End_H"))
    start_time_m = NumTextBox(app.event_start_t_m[0],
    "0", SE_layout_manager(app, "Start_M"))
    end_time_m = NumTextBox(app.event_end_t_m[0],
    "0", SE_layout_manager(app, "End_M"))
    app.SE_btns['Year'] = app.FE_btns['Year1'] = app.RE_btns['Year1'] = year1
    app.SE_btns['Month'] = app.FE_btns['Month1'] = app.RE_btns['Month1'] = month1
    app.SE_btns['Day'] = app.FE_btns['Day1'] = app.RE_btns['Day1']  = day1
    app.FE_btns['Year2'] = app.RE_btns['Year2'] = NumTextBox("Year2",
    app.currentDate.year, RE_and_FE_layout_manager(app, "Year2"))
    app.FE_btns['Month2'] = app.RE_btns['Month2'] = NumTextBox("Month2",
    app.currentDate.month, RE_and_FE_layout_manager(app, "Month2"))
    app.FE_btns['Day2'] = app.RE_btns['Day2']  = NumTextBox("Day2",
    app.currentDate.day, RE_and_FE_layout_manager(app, "Day2"))
    app.SE_btns['Start_H'] = app.FE_btns['Start_H'] = app.RE_btns['Start_H'] = start_time_h
    app.SE_btns['End_H'] = app.RE_btns['End_H'] = end_time_h
    app.SE_btns['Start_M'] = app.FE_btns['Start_M'] = app.RE_btns['Start_M'] = start_time_m
    app.SE_btns['End_M'] = app.RE_btns['End_M'] = end_time_m
    app.FE_btns['Num_Days'] = NumTextBox("Num_Days",
    "1", FE_layout_manager(app, "Num_Days"))
    for i in ["sun", "mon", "tue", "wed", "th", "fri", "sat"]:
        app.RE_btns['Week_Days'][i] = RectButton(i,
        i, i, RE_layout_manager(app, i))

def change_screen_size(app):
    #changes screensize of buttons
    app.event_always_btns['title'].set_coord(create_event_layout_manager(app, 'title'))
    app.event_always_btns['description'].set_coord(create_event_layout_manager(app, 'description'))
    app.event_always_btns['SE'].set_coord(selector_panel_layout_manager(app, "SE"))
    app.event_always_btns['RE'].set_coord(selector_panel_layout_manager(app, "RE"))
    app.event_always_btns['FE'].set_coord(selector_panel_layout_manager(app, "FE"))
    app.event_always_btns['save'].set_coord(save_layout_manager(app, "save"))

def clicked_within(x, y, coord):
    #checks if x and y are within the coordinates
    if x >= coord[0] and x <= coord[2] and y >= coord[1] and y <= coord[3]:
        return True

def get_clicked_item(app, x, y):
    #returns button that is clicked
    if clicked_within(x, y, app.event_always_btns['title'].get_coord()):
        return app.event_always_btns['title']
    elif clicked_within(x, y, app.event_always_btns['description'].get_coord()):
        return app.event_always_btns['description']
    elif clicked_within(x, y, app.event_always_btns['RE'].get_coord()):
        return app.event_always_btns['RE']
    elif clicked_within(x, y, app.event_always_btns['SE'].get_coord()):
        return app.event_always_btns['SE']
    elif clicked_within(x, y, app.event_always_btns['FE'].get_coord()):
        return app.event_always_btns['FE']
    elif clicked_within(x, y, app.event_always_btns['save'].get_coord()):
        return app.event_always_btns['save']
    if app.current_event_panel == "SE":
        for btn in app.SE_btns:
            if clicked_within(x, y, app.SE_btns[btn].get_coord()):
                return app.SE_btns[btn]
    elif app.current_event_panel == "RE":
        for btn in app.RE_btns:
            if btn != "Week_Days":
                if clicked_within(x, y, app.RE_btns[btn].get_coord()):
                    return app.RE_btns[btn]
        for days in app.RE_btns["Week_Days"]:
            if clicked_within(x, y, app.RE_btns["Week_Days"][days].get_coord()):
                    return app.RE_btns["Week_Days"][days]
    elif app.current_event_panel == "FE":
        for btn in app.FE_btns:
            if clicked_within(x, y, app.FE_btns[btn].get_coord()):
                return app.FE_btns[btn]