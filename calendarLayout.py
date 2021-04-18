from cmu_112_graphics import *
from inputBox import * 

##############################
#LAYOUT MANAGERS
##############################

def layout_manager(app, panel):
    #organizes layout and returns panel coordinates
    layoutBoundsX0 = layoutBoundsY0 = app.margin 
    layoutBoundsX1 = app.width - app.margin
    layoutBoundsY1 = app.height - app.margin
    layoutHeight = layoutBoundsY1 - layoutBoundsY0
    layoutWidth = layoutBoundsX1 - layoutBoundsX0

    leftPanelHeight = rightPanelHeight = layoutHeight - app.layoutSpacing
    leftPanelWidth = (layoutWidth - app.layoutSpacing) * .85
    rightPanelWidth = (layoutWidth - app.layoutSpacing) * .15
    bottomPanelsY0 = layoutBoundsY0
    if panel == "left_panel":
        return (layoutBoundsX0, bottomPanelsY0, layoutBoundsX0 + leftPanelWidth, 
        layoutBoundsY1)
    elif panel == "right_panel":
        x0 = layoutBoundsX0 + leftPanelWidth + app.layoutSpacing
        return (x0, bottomPanelsY0, layoutBoundsX1, layoutBoundsY1)

def left_panel_manager(app, component):
    x0, y0, x1, y1 = layout_manager(app, "left_panel")
    calendarHeight = (y1 - y0) * .85
    selectorHeight = (y1 - y0) * .15
    if component == "calendar_view":
        return (x0, y0, x1, y0 + calendarHeight)
    elif component == "date_selector":
        return (x0, y0 + calendarHeight, x1, y1)
    '''
    calendarHeight = (y1 - y0 - app.layoutSpacing) * .9
    selectorHeight = (y1 - y0 - app.layoutSpacing) * .1
    if component == "calendar_view":
        return (x0, y0, x1, y0 + calendarHeight)
    elif component == "date_selector":
        return (x0, y0 + calendarHeight + app.layoutSpacing, x1, y1)'''

def calendar_view_manager(app, component):
    x0, y0, x1, y1 = left_panel_manager(app, "calendar_view")
    titleHeight = (y1 - y0) * .15
    if component == "title":
        return (x0, y0, x1, y0 + titleHeight)
    elif component == "calendar":
        return (x0, y0 + titleHeight, x1, y1)

def calendar_inner_bounds(app, component):
    x0, y0, x1, y1 = calendar_view_manager(app, "calendar")
    timesWidth = (x1 - x0) * .12
    if component == "times":
        return (x0 + app.calendarPadding, y0 + app.calendarPadding, 
        x0 + timesWidth, y1 - app.calendarPadding)
    elif component == "event":
        return (x0 + timesWidth, y0 + app.calendarPadding, 
        x1 - app.calendarPadding, y1 - app.calendarPadding)

def get_row_bounds(app, row, y0, y1):
    newY0 = y0 + ((y1 - y0) // app.hoursViewed) * row
    newY1 = y0 + ((y1 - y0) // app.hoursViewed) * (row + 1)
    return (newY0, newY1)

def get_col_bounds(app, col, x0, x1):
    newX0 = x0 + ((x1 - x0) // app.cols) * col
    newX1 = x0 + ((x1 - x0) // app.cols) * (col + 1)
    return (newX0, newX1)

def get_row_and_col_bounds(app, row, col, x0, x1, y0, y1):
    y0, y1 = get_row_bounds(app, row, y0, y1)
    x0, x1 = get_col_bounds(app, col, x0, x1)
    return (x0, y0, x1, y1)

def calendar_option_btns(app, init):
    x0, y0, x1, y1 = layout_manager(app, "right_panel")
    padding = 20
    btnHeight = 40
    i = 0
    if init:
        for name, redirect in app.calOptions:
            newX0, newY0, newX1, newY1 = (x0 + padding, 
            y0 + padding*(i+1) + btnHeight*i, x1 - padding, 
            y0 + padding*(i+1) + btnHeight*(i+1))
            app.calOptionBtnObject.append(RectButton(name, redirect, (newX0, newY0,
            newX1, newY1)))
            i += 1
    else:
        for button in app.calOptionBtnObject:
            newX0, newY0, newX1, newY1 = (x0 + padding, 
            y0 + padding*(i+1) + btnHeight*i, x1 - padding, 
            y0 + padding*(i+1) + btnHeight*(i+1))
            button.set_coord((newX0, newY0, newX1, newY1))
            i += 1

def calendar_select_input(app, init):
    x0, y0, x1, y1 = left_panel_manager(app, "date_selector")
    padding = 20
    btnHeight = 50
    i = 0
    yearX0
    if init:
        for name, default in app.calSelects:
            newX0, newY0, newX1, newY1 = (x0 + padding, 
            y0 + padding*(i+1) + btnHeight*i, x1 - padding, 
            y0 + padding*(i+1) + btnHeight*(i+1))
            app.calOptionBtnObject.append(RectButton(name, redirect, (newX0, newY0,
            newX1, newY1)))
            i += 1
    else:
        for button in app.calOptionBtnObject:
            newX0, newY0, newX1, newY1 = (x0 + padding, 
            y0 + padding*(i+1) + btnHeight*i, x1 - padding, 
            y0 + padding*(i+1) + btnHeight*(i+1))
            button.set_coord((newX0, newY0, newX1, newY1))
            i += 1