from cmu_112_graphics import *
from calendarLayout import *
from inputBox import * 

##############################
# DRAWING
##############################

######### CALENDAR VIEW #########
def draw_title_headers(app, canvas, x0, y0, x1, y1):
    if app.calendarMode == "week":
        newX0, newY0, newX1, newY1 = calendar_inner_bounds(app, "event")
        dayOffset = 0
        if len(app.currentWeek) < 7 and app.currentWeek[0][1].day == 1:
            dayOffset = 7 - len(app.currentWeek) 
        for i in range(len(app.currentWeek)):
            x0, x1 = get_col_bounds(app, i + dayOffset, newX0, newX1)
            middleX = x0 + (x1 - x0) / 2
            line1 = y0 + (y1 - y0) * (1/3)
            line2 = y0 + (y1 - y0) * (2/3)
            canvas.create_text(middleX, line1, text=app.currentWeek[i][0],
            anchor="c", font="Ariel 20")
            canvas.create_text(middleX, line2, text=app.currentWeek[i][1].day,
            anchor="c", font="Ariel 20")
            canvas.create_rectangle(x0, y0, x1, y1)

def draw_title_side_box(app, canvas, y0, y1, titlePadding):
    newX0, newY0, newX1, newY1 = calendar_inner_bounds(app, "times")
    boxPadding = 10
    x0, y0, x1, y1 = (newX0 + boxPadding, y0 + boxPadding, 
    newX1 - titlePadding - boxPadding, y1 - boxPadding)
    canvas.create_rectangle(x0, y0, x1, y1)
    middleX = x0 + (x1 - x0) // 2
    if app.calendarMode == "week":
        canvas.create_text(middleX, y0, text=app.currentDate.year,
        anchor="n", font="Ariel 20")
        canvas.create_text(middleX, y1, text=app.months[app.currentDate.month 
        - 1],
        anchor="s", font="Ariel 20")

def draw_week_view_title(app, canvas):
    x0, y0, x1, y1 = calendar_view_manager(app, "title")
    canvas.create_rectangle(x0, y0, x1, y1, fill="pink", width=0)
    titlePadding = 10
    draw_title_headers(app, canvas, x0 + titlePadding, y0 + titlePadding, 
    x1 - titlePadding, y1 - titlePadding)
    draw_title_side_box(app, canvas, y0 + titlePadding, y1 - titlePadding, 
    titlePadding)

def draw_times(app, canvas, x0, y0, x1, y1):
    timeX0, timeY0, timeX1, timeY1 = calendar_inner_bounds(app, "times")
    #canvas.create_rectangle(timeX0, timeY0, timeX1, timeY1, fill="lightgreen")
    eventX0, eventY0, eventX1, eventY1 = calendar_inner_bounds(app, "event")
    for i in range(len(app.shownHours)):
        newY0, newY1 = get_row_bounds(app, i, timeY0, timeY1)
        canvas.create_text(timeX0, newY0, text=app.shownHours[i], anchor="w")
        canvas.create_line(eventX0, newY0, eventX1, newY0)

def shown_event(app, cal_event):
    if (is_time_greater(cal_event['end_time'], app.shownHours[0]) and 
    is_time_greater(app.shownHours[0], cal_event['start_time'])):
        return "end_shown"
    elif (is_time_greater(app.shownHours[-1], cal_event['start_time']) and
    is_time_greater(app.shownHours[0], cal_event['start_time'])):
        return "start_shown"
    else: 
        return None

def draw_cells(app, canvas, x0, y0, x1, y1):
    x0, y0, x1, y1 = calendar_inner_bounds(app, "event")
    for cal_event in app.schedule:
        bounds = get_event_bounds(app, cal_event, x0, y0, x1, y1)
        if bounds != None:
            newX0, newY0, newX1, newY1 = bounds 
            canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="pink")
            canvas.create_text(newX0, newY0, anchor="nw", 
            text=cal_event["title"])
    '''
    for j in range(7):
        for i in range(len(app.shownHours)):
            newX0, newY0, newX1, newY1 = get_row_and_col_bounds(app, i, j, x0, 
            x1, y0, y1)
            canvas.create_rectangle(newX0, newY0, newX1, newY1)'''

def draw_week_view_calendar(app, canvas):
    x0, y0, x1, y1 = calendar_view_manager(app, "calendar")
    canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", width=0)
    draw_times(app, canvas, x0, y0, x1, y1)
    draw_cells(app, canvas, x0, y0, x1, y1)
    

def draw_week_view(app, canvas):
    draw_week_view_title(app, canvas)
    draw_week_view_calendar(app, canvas)

def draw_month_view(app, canvas):
    x0, y0, x1, y1 = left_panel_manager(app, "calendar_view")
    canvas.create_rectangle(x0, y0, x1, y1, fill="grey", width=0)

def draw_year_view(app, canvas):
    x0, y0, x1, y1 = left_panel_manager(app, "calendar_view")
    canvas.create_rectangle(x0, y0, x1, y1, fill="grey", width=0)

######### SELECTOR #########
def draw_date_selector(app, canvas):
    x0, y0, x1, y1 = left_panel_manager(app, "date_selector")
    canvas.create_rectangle(x0, y0, x1, y1, fill="grey", width=0)
    for button in app.calSelectorMoveBtns:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="pink")
        canvas.create_text(middleX, middleY, text=button.get_value(),
        font="Ariel 25")
    for button in app.calSelectorInputs:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="pink")
        canvas.create_text(middleX, middleY, text=button.get_value(),
        font="Ariel 25")

######### OPTIONS #########
def draw_options(app, canvas):
    x0, y0, x1, y1 = layout_manager(app, "right_panel")
    canvas.create_rectangle(x0, y0, x1, y1, fill="grey", width=0)
    for button in app.calOptionBtnObject:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="pink")
        canvas.create_text(middleX, middleY, text=button.get_value())

##############################
# REDRAW ALL
##############################

def calendarHome_redrawAll(app, canvas):
    if app.calendarMode == "week":
        draw_week_view(app, canvas)
    elif app.calendarMode == "month":
        draw_month_view(app, canvas)
    elif app.calendarMode == "year":
        draw_year_view(app, canvas)
    draw_date_selector(app, canvas)
    draw_options(app, canvas)
