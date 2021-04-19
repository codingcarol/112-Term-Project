from cmu_112_graphics import *
from inputBox import * 
from typing import *
from date_functions import *
from calendarDraw import *

##############################
# CONTROLS
##############################

def calendarHome_keyPressed(app, event):
    if app.typing:
        typing_event(app, event)
        return
    if event.key == "Up" and app.firstHour > 0:
        app.firstHour -= 1
        app.lastHour = app.firstHour + app.hoursViewed
        app.shownHours = app.hours[app.firstHour:app.lastHour]
    elif event.key == "Down" and app.lastHour < len(app.hours):
        app.firstHour += 1
        app.lastHour = app.firstHour + app.hoursViewed
        app.shownHours = app.hours[app.firstHour:app.lastHour]

def clicked_within(x, y, coord):
    if x >= coord[0] and x <= coord[2] and y >= coord[1] and y <= coord[3]:
        return True

def get_clicked_item(app, x, y):
    if clicked_within(x, y, layout_manager(app, "right_panel")):
        item = get_right_panel_btn(app, x, y)
        return item
    elif clicked_within(x, y, left_panel_manager(app, "date_selector")):
        item = get_dates_panel_btn(app, x, y)
        return item
    elif clicked_within(x, y, calendar_view_manager(app, "calendar")):
        return "calendar"

def get_right_panel_btn(app, x, y):
    for button in app.calOptionBtnObject:
        if clicked_within(x, y, button.get_coord()):
            return button

def get_dates_panel_btn(app, x, y):
    for button in app.calSelectorMoveBtns:
        if clicked_within(x, y, button.get_coord()):
            return button
    for inputs in app.calSelectorInputs:
        if clicked_within(x, y, inputs.get_coord()):
            app.typing = True
            return inputs

def go_btn(app):
    year = app.calSelectorInputs[0].get_value()
    month = app.calSelectorInputs[1].get_value()
    day = app.calSelectorInputs[2].get_value()
    change_current_date(app, year, month, day, False)

def left_btn(app):
    year, month, day = get_previous_week_date(app, app.currentWeek)
    change_current_date(app, year, month, day, True)

def right_btn(app):
    year, month, day = get_next_week_date(app, app.currentWeek)
    change_current_date(app, year, month, day, True)

def see_today(app):
    d = get_current_date()
    year, month, day = d.year, d.month, d.day
    change_current_date(app, year, month, day, False)

def calendarHome_mousePressed(app, event):
    reset_typing_setting(app)
    item = get_clicked_item(app, event.x, event.y)
    if type(item) == RectButton:
        app.recentBtn = item.name
        if item.name == "Go":
            go_btn(app)
        if item.name == "Left":
            left_btn(app)
        if item.name == "Right":
            right_btn(app)
        if item.name == "See Today":
            see_today(app)
        #app.mode = item.get_redirect()
    elif type(item) == NumTextBox:
        app.typing = True
        app.text_box = item

def calendarHome_sizeChanged(app):
    calendar_option_btns(app, False)
    calendar_select_input(app, False)
