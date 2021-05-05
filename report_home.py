import csv
from event_functions import *
from inputBox import *
import string
from typing import *
from datetime import date
from date_functions import *
from create_event_layout_manager import get_button_x

def create_report_layout_manager(app, component):
    #layout manager for the report page
    layoutBoundsX0 = x0 = app.event_paddingX
    layoutBoundsY0 = app.event_paddingY
    layoutBoundsX1 = app.width - app.event_paddingX
    layoutBoundsY1 = app.height - app.event_paddingY
    layoutHeight = layoutBoundsY1 - layoutBoundsY0
    width = layoutBoundsX1 - layoutBoundsX0
    total_padding = app.event_inner_padding * 4
    total_height = layoutHeight - total_padding
    title_height = total_height * .1
    time_title_height = missed_title_height = total_height * .1
    date_height = total_height *.1
    title_y0 = layoutBoundsY0
    title_y1 = title_y0 + title_height
    d_y0 = title_y1 + app.event_inner_padding
    d_y1 = date_height + d_y0
    d_button_length = 100
    time_title_y0 = d_y1 + app.event_inner_padding
    time_title_y1 = time_title_height + time_title_y0
    t_y0 = time_title_y1 + app.event_inner_padding
    t_y1 = t_y0 + total_height *.1
    time_button_length = width * .1
    missed_title_y0 =  t_y1 + app.event_inner_padding
    missed_title_y1 = missed_title_height +  missed_title_y0
    missed_y0 = missed_title_y1 + app.event_inner_padding
    missed_y1 = missed_y0 + total_height *.1
    save_y0 = missed_y1 + app.event_inner_padding
    save_y1 = save_y0 + total_height *.1
    if component == "title":
        return (layoutBoundsX0, title_y0, layoutBoundsX1, title_y1)
    elif component == "year":
        new_x0, new_x1 = get_button_x(x0, 0, 3, d_button_length, 20, width)
        return (new_x0, d_y0, new_x1, d_y1)
    elif component == "month":
        new_x0, new_x1 = get_button_x(x0, 1, 3, d_button_length, 20, width)
        return (new_x0, d_y0, new_x1, d_y1)
    elif component == "day":
        new_x0, new_x1 = get_button_x(x0, 2, 3, d_button_length, 20, width)
        return (new_x0, d_y0, new_x1, d_y1)
    elif component == "start_t_H":
        new_x0, new_x1 = get_button_x(x0, 0, 2, time_button_length, 30, width)
        return new_x0, t_y0, new_x1, t_y1
    elif component == "start_t_M":
        new_x0, new_x1 = get_button_x(x0, 1, 2, time_button_length, 30, width)
        return new_x0, t_y0, new_x1, t_y1
    elif component == "missed":
        new_x0, new_x1 = get_button_x(x0, 0, 2, time_button_length, 30, width)
        return (new_x0 - 60, missed_y0, new_x1 - 60, missed_y1)
    elif component == "mood":
        new_x0, new_x1 = get_button_x(x0, 1, 2, time_button_length, 30, width)
        return (new_x0 + 60, missed_y0, new_x1 + 60, missed_y1)
    elif component == "save":
        return (layoutBoundsX0, save_y0 + 20, layoutBoundsX1, save_y1 + 20)

def create_record_input(app):
    #creates the buttons for the report page
    app.record_btns['title'] = TextBox('title', 'event name', create_report_layout_manager(app, 'title'),
    string.printable)
    app.record_btns['save'] = RectButton('save', 'save', 'save', create_report_layout_manager(app, 'save'))
    app.record_btns['year'] = NumTextBox('year', app.currentDate.year, create_report_layout_manager(app, 'year'))
    app.record_btns['month'] = NumTextBox('month', app.currentDate.month, create_report_layout_manager(app, 'month'))
    app.record_btns['day'] = NumTextBox('day', app.currentDate.day, create_report_layout_manager(app, 'day'))
    app.record_btns['start_t_H'] = NumTextBox('start_t_H', "13", create_report_layout_manager(app, 'start_t_H'))
    app.record_btns['start_t_M'] = NumTextBox('start_t_M', "30", create_report_layout_manager(app, 'start_t_M'))
    app.record_btns['missed'] = TextBox('missed', "p", create_report_layout_manager(app, 'missed'), string.ascii_lowercase)
    app.record_btns['mood'] = NumTextBox('mood', "5", create_report_layout_manager(app, 'mood'))

def clicked_within(x, y, coord):
    #checks if the x y values are within the coordinates
    if x >= coord[0] and x <= coord[2] and y >= coord[1] and y <= coord[3]:
        return True

def get_clicked_item(app, x, y):
    #returns the clicked item
    for btn in app.record_btns:
        if clicked_within(x, y, app.record_btns[btn].get_coord()):
            return app.record_btns[btn]

def report_keyPressed(app, event):
    #controls behavior on report page when a key is pressed 
    if app.typing and (type(app.text_box) == TextBox or type(app.text_box) == NumTextBox):
        typing_event(app, event)
        return
    if event.key == "Escape":
        app.mode = "calendarHome"

def report_mousePressed(app, event):
    #controls behavior on report page when mouse is clicked
    reset_typing_setting(app)
    item = get_clicked_item(app, event.x, event.y)
    if type(item) == RectButton:
        if item.name == "save":
            save_btn(app)
    elif type(item) == TextBox or type(item) == NumTextBox:
        app.typing = True
        app.text_box = item

def save_btn(app):
    #save button behavior 
    title = app.record_btns['title'].get_value()
    year =  app.record_btns['year'].get_value()
    month =  app.record_btns['month'].get_value()
    day =  app.record_btns['day'].get_value()
    start_t_H = app.record_btns['start_t_H'].get_value()
    start_t_M = app.record_btns['start_t_M'].get_value()
    start_time = make_into_time_str(start_t_H, start_t_M)
    missed = app.record_btns['missed'].get_value()
    mood = app.record_btns['mood'].get_value()
    flex_event_dict = get_all_flex(app.schedule_folder)
    if title not in flex_event_dict: return
    if not time_is_valid(start_t_H, start_t_M): return
    duration = flex_event_dict[title]['duration']
    same_day, end_time = add_duration_to_time(start_time, duration)
    if not same_day: return 
    if missed != 'm' and missed != 'p':
        return 
    if missed == "m":
        missed = "missed"
    else:
        missed = "present"
    d_date = nearest_valid_date(app, int(year), int(month), int(day))
    mood = int(mood)
    weekdays = ['sun', 'mon', 'tue', 'wed', 'th', 'fri', 'sat']
    d =  weekdays[get_week_day_index(d_date)]
    all_flex = get_all_flex(app.schedule_folder)
    event_titles = all_flex.keys()
    if title not in event_titles:
        return 
    if not is_strictly_time_greater(end_time, start_time):
        return
    event_id = all_flex[title]['id']
    with open(f'data/{app.schedule_folder}/flexible_event_records/{event_id}.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([d_date,d,start_time,end_time,missed,mood])

def report_redrawAll(app, canvas):
    #draws all the report buttons
    time_y0 = 0
    time_y1 = 0
    start_H_x0 = 0
    start_H_x1 = 0
    start_M_x0 = 0
    start_M_x1 = 0
    for btn in app.record_btns:
        x0, y0, x1, y1 = app.record_btns[btn].get_coord()
        canvas.create_rectangle(x0, y0, x1, y1, fill="#cfecff")
        x = x0 + (x1 - x0)/2
        y = y0 + (y1 - y0)/2
        canvas.create_text(x, y, text=app.record_btns[btn].get_value(),
        font="Ariel 20") 
        if btn == "missed":
            canvas.create_text(x, y0 - 10, text="missed/present \n(m or p)",
            font="Ariel 14", anchor="s")
        if btn == "mood":
            canvas.create_text(x, y0 - 10, text="mood \n(1 to 10)",
            font="Ariel 14", anchor="s")
        if btn == "start_t_H":
            time_y0 = y0
            time_y1 = y1
            start_H_x0 = x0
            start_H_x1 = x1
        elif btn == "start_t_M":
            start_M_x0 = x0
            start_M_x1 = x1
        elif btn == "end_t_H":
            end_H_x0 = x0
            end_H_x1 = x1
        elif btn == "end_t_M":
            end_M_x0 = x0
            end_M_x1 = x1
    canvas.create_text((start_H_x0 + start_M_x1) / 2, time_y0 - 20, 
    text="Start Time", anchor="s", font="Ariel 20")
    canvas.create_text((start_H_x1 + start_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")

def get_all_flex(schedule_folder):
    #gets all the flex events ids, returns a dictionary of event title, id 
    flex = {}
    with open(get_flex_events_csv(schedule_folder), newline='') as csv_file:
    # CITATION: https://docs.python.org/3/library/csv.html
        reader = csv.DictReader(csv_file)
        for row in reader:
            flex[row['title']] = {'id': row['id'], 'duration': row['duration']}
    return flex