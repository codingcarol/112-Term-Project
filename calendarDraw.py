from cmu_112_graphics import *
from calendarLayout import *
from inputBox import * 

##############################
# DRAWING
##############################

######### CALENDAR VIEW #########
def draw_title_headers(app, canvas, x0, y0, x1, y1):
    #draws the titles for the days of week (i.e. Sun, Mon, Tue...)
    if app.calendarMode == "week":
        newX0, newY0, newX1, newY1 = calendar_inner_bounds(app, "event")
        dayOffset = 0
        if len(app.currentWeek) < 7 and app.currentWeek[0][1].day == 1:
            dayOffset = 7 - len(app.currentWeek) 
        for i in range(len(app.currentWeek)): #write day and day of week for the entire week
            x0, x1 = get_col_bounds(app, i + dayOffset, newX0, newX1)
            middleX = x0 + (x1 - x0) / 2
            line1 = y0 + (y1 - y0) * (1/3)
            line2 = y0 + (y1 - y0) * (2/3)
            canvas.create_text(middleX, line1, text=app.currentWeek[i][0],
            anchor="c", font="Ariel 20")
            canvas.create_text(middleX, line2, text=app.currentWeek[i][1].day,
            anchor="c", font="Ariel 20")

def draw_title_side_box(app, canvas, y0, y1, titlePadding):
    #draws the year and month in top left corner
    newX0, newY0, newX1, newY1 = calendar_inner_bounds(app, "times")
    boxPadding = 10
    x0, y0, x1, y1 = (newX0 + boxPadding, y0 + boxPadding, 
    newX1 - titlePadding - boxPadding, y1 - boxPadding)
    middleX = x0 + (x1 - x0) // 2
    if app.calendarMode == "week":
        canvas.create_text(middleX, y0, text=app.currentDate.year,
        anchor="n", font="Ariel 20")
        canvas.create_text(middleX, y1, text=app.months[app.currentDate.month 
        - 1],
        anchor="s", font="Ariel 20")

def draw_week_view_title(app, canvas):
    #draws the background panel behind the weekday header
    x0, y0, x1, y1 = calendar_view_manager(app, "title")
    canvas.create_rectangle(x0, y0, x1, y1, fill="#cfecff", width=0)
    titlePadding = 10
    draw_title_headers(app, canvas, x0 + titlePadding, y0 + titlePadding, 
    x1 - titlePadding, y1 - titlePadding)
    draw_title_side_box(app, canvas, y0 + titlePadding, y1 - titlePadding, 
    titlePadding)

def draw_times(app, canvas, x0, y0, x1, y1):
    #draws the times in the left column
    timeX0, timeY0, timeX1, timeY1 = calendar_inner_bounds(app, "times")
    eventX0, eventY0, eventX1, eventY1 = calendar_inner_bounds(app, "event")
    for i in range(len(app.shownHours)):
        newY0, newY1 = get_row_bounds(app, i, timeY0, timeY1)
        canvas.create_text(timeX0, newY0, text=app.shownHours[i], anchor="w")
        canvas.create_line(eventX0, newY0, eventX1, newY0)

def draw_cells(app, canvas, x0, y0, x1, y1):
    #draws each event block
    x0, y0, x1, y1 = calendar_inner_bounds(app, "event")
    for cal_event in app.schedule:
        bounds = get_event_bounds(app, cal_event, x0, y0, x1, y1)
        if bounds != None:
            newX0, newY0, newX1, newY1 = bounds 
            canvas.create_rectangle(newX0, newY0, newX1, newY1, 
            fill="#cfecff", width=1)
            canvas.create_text((newX0 + newX1)/2, newY0 + 5, anchor="n", 
            text=cal_event["title"])

def draw_week_view_calendar(app, canvas):
    #draws the calendar part of the UI
    x0, y0, x1, y1 = calendar_view_manager(app, "calendar")
    draw_times(app, canvas, x0, y0, x1, y1)
    draw_cells(app, canvas, x0, y0, x1, y1)

def draw_week_view(app, canvas):
    #draws the entire calendar panel + header
    draw_week_view_title(app, canvas)
    draw_week_view_calendar(app, canvas)

######### SELECTOR #########
def draw_date_selector(app, canvas):
    #draws the selector panel (choose the date)
    x0, y0, x1, y1 = left_panel_manager(app, "date_selector")
    canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=1)
    for button in app.calSelectorMoveBtns:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="#cfecff",
        width=1)
        canvas.create_text(middleX, middleY, text=button.get_value(),
        font="Ariel 25")
    for button in app.calSelectorInputs:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="#cfecff",
        width=1)
        canvas.create_text(middleX, middleY, text=button.get_value(),
        font="Ariel 25")

######### OPTIONS #########
def draw_options(app, canvas):
    #draw options panel
    x0, y0, x1, y1 = layout_manager(app, "right_panel")
    canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=0)
    for button in app.calOptionBtnObject:
        newX0, newY0, newX1, newY1 = button.get_coord()
        middleX = newX0 + (newX1 - newX0)/2
        middleY = newY0 + (newY1 - newY0)/2
        canvas.create_rectangle(newX0, newY0, newX1, newY1, fill="#cfecff")
        canvas.create_text(middleX, middleY, text=button.get_value())

##############################
# REDRAW ALL
##############################

def calendarHome_redrawAll(app, canvas):
    #draws the calendar page
    if app.calendarMode == "week":
        draw_week_view(app, canvas)
    draw_date_selector(app, canvas)
    draw_options(app, canvas)
