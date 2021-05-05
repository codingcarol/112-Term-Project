from inputBox import *
from create_event_layout_manager import *

def draw_btns(app, canvas):
    #draws regular buttons on event page
    for btn in app.event_always_btns:
        x0, y0, x1, y1 = app.event_always_btns[btn].get_coord()
        fill = "#cfecff"
        if btn == "SE": #SE, RE, FE are different colored buttons
            fill = "#e7ffde"
        elif btn == "RE":
            fill = "#dee1ff"
        elif btn == "FE":
            fill = "#ffebfd"
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        if isinstance(app.event_always_btns[btn], RectButton):
            x = x0 + (x1 - x0)/2
            y = y0 + (y1 - y0)/2
            canvas.create_text(x, y, text=app.event_always_btns[btn].get_value(),
            font="Ariel 20")
        elif isinstance(app.event_always_btns[btn], TextBox):
            y = y0 + (y1 - y0)/2
            x = x0 + 20
            if btn == "title":
                font = "Ariel 20"
                anchor = "w"
            elif btn == "description":
                y = y0 + 20
                font = "Ariel 16"
                anchor = "nw"
            canvas.create_text(x, y, text=app.event_always_btns[btn].get_value(),
            anchor=anchor, font=font)

def draw_options_panel(app, canvas):
    #draws options panel, (outline of where you put the date, time, etc.)
    x0, y0, x1, y1 = create_event_layout_manager(app, 'options')
    canvas.create_rectangle(x0, y0, x1, y1)

def draw_SE_btns(app, canvas):
    #draws strict event buttons
    time_y0 = 0
    time_y1 = 0
    start_H_x0 = 0
    start_H_x1 = 0
    start_M_x0 = 0
    start_M_x1 = 0
    end_H_x0 = 0
    end_H_x1 = 0
    end_M_x0 = 0
    end_M_x1 = 0
    for btn in app.SE_btns: #draws the buttons
        x0, y0, x1, y1 = app.SE_btns[btn].get_coord()
        canvas.create_rectangle(x0, y0, x1, y1, fill="#e7ffde")
        x = x0 + (x1 - x0)/2
        y = y0 + (y1 - y0)/2
        canvas.create_text(x, y, text=app.SE_btns[btn].get_value(),
            font="Ariel 20")
        if btn == "Start_H":
            time_y0 = y0
            time_y1 = y1
            start_H_x0 = x0
            start_H_x1 = x1
        elif btn == "Start_M":
            start_M_x0 = x0
            start_M_x1 = x1
        elif btn == "End_H":
            end_H_x0 = x0
            end_H_x1 = x1
        elif btn == "End_M":
            end_M_x0 = x0
            end_M_x1 = x1
    #draws text and labels
    canvas.create_text((start_H_x0 + start_M_x1) / 2, time_y0 - 20, 
    text="Start Time", anchor="s", font="Ariel 20")
    canvas.create_text((end_H_x0 + end_M_x1) / 2, time_y0 - 20, 
    text="End Time", anchor="s", font="Ariel 20")
    canvas.create_text((start_H_x1 + start_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")
    canvas.create_text((end_H_x1 + end_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")

def draw_RE_btns(app, canvas):
    #draws recurring event buttons
    time_y0 = 0
    time_y1 = 0
    start_H_x0 = 0
    start_H_x1 = 0
    start_M_x0 = 0
    start_M_x1 = 0
    end_H_x0 = 0
    end_H_x1 = 0
    end_M_x0 = 0
    end_M_x1 = 0
    for btn in app.RE_btns: #draws buttons
        if btn != "Week_Days":
            x0, y0, x1, y1 = app.RE_btns[btn].get_coord()
            canvas.create_rectangle(x0, y0, x1, y1, fill="#dee1ff")
            x = x0 + (x1 - x0)/2
            y = y0 + (y1 - y0)/2
            canvas.create_text(x, y, text=app.RE_btns[btn].get_value(),
                font="Ariel 20")
            if btn == "Start_H":
                time_y0 = y0
                time_y1 = y1
                start_H_x0 = x0
                start_H_x1 = x1
            elif btn == "Start_M":
                start_M_x0 = x0
                start_M_x1 = x1
            elif btn == "End_H":
                end_H_x0 = x0
                end_H_x1 = x1
            elif btn == "End_M":
                end_M_x0 = x0
                end_M_x1 = x1
    for day in app.RE_btns["Week_Days"]: #draws weekday buttons
        x0, y0, x1, y1 = app.RE_btns["Week_Days"][day].get_coord()
        canvas.create_rectangle(x0, y0, x1, y1, fill=app.RE_btns["Week_Days"][day].get_fill())
        x = x0 + (x1 - x0)/2
        y = y0 + (y1 - y0)/2
        canvas.create_text(x, y, text=app.RE_btns["Week_Days"][day].get_value(),
            font="Ariel 16")
    #draws text and labels
    canvas.create_text((start_H_x0 + start_M_x1) / 2, time_y0 - 20, 
    text="Start Time", anchor="s", font="Ariel 20")
    canvas.create_text((end_H_x0 + end_M_x1) / 2, time_y0 - 20, 
    text="End Time", anchor="s", font="Ariel 20")
    canvas.create_text((start_H_x1 + start_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")
    canvas.create_text((end_H_x1 + end_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")

def draw_FE_btns(app, canvas):
    #draws flexible event buttons
    time_y0 = 0
    time_y1 = 0
    start_H_x0 = 0
    start_H_x1 = 0
    start_M_x0 = 0
    start_M_x1 = 0
    for btn in app.FE_btns: #draws buttons
        x0, y0, x1, y1 = app.FE_btns[btn].get_coord()
        canvas.create_rectangle(x0, y0, x1, y1, fill="#ffebfd")
        x = x0 + (x1 - x0)/2
        y = y0 + (y1 - y0)/2
        canvas.create_text(x, y, text=app.FE_btns[btn].get_value(),
            font="Ariel 20")
        if btn == "Start_H":
            time_y0 = y0
            time_y1 = y1
            start_H_x0 = x0
            start_H_x1 = x1
        elif btn == "Start_M":
            start_M_x0 = x0
            start_M_x1 = x1
    #draws text and labels
    canvas.create_text((start_H_x0 + start_M_x1) / 2, time_y0 - 20, 
    text="Duration", anchor="s", font="Ariel 20")
    canvas.create_text((start_H_x1 + start_M_x0) / 2, (time_y0 + time_y1)/2, 
    text=":", font="Ariel 20")

def createEvent_redrawAll(app, canvas):
    #draws everything on the event page
    draw_options_panel(app, canvas)
    draw_btns(app, canvas)
    if app.current_event_panel == "SE":
        draw_SE_btns(app, canvas)
    elif app.current_event_panel == "RE":
        draw_RE_btns(app, canvas)
    elif app.current_event_panel == "FE":
        draw_FE_btns(app, canvas)  