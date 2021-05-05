
def create_event_layout_manager(app, component):
    #event page layout manager
    layoutBoundsX0 = app.event_paddingX
    layoutBoundsY0 = app.event_paddingY
    layoutBoundsX1 = app.width - app.event_paddingX
    layoutBoundsY1 = app.height - app.event_paddingY
    layoutHeight = layoutBoundsY1 - layoutBoundsY0
    layoutWidth = layoutBoundsX1 - layoutBoundsX0
    total_padding = app.event_inner_padding * 4
    total_height = layoutHeight - total_padding
    title_height = total_height * .1
    description_height = total_height * .2
    selector_height = total_height * .1
    options_height = total_height * .5
    save_height = total_height * .1
    #coordinates of each component
    title_y0 = layoutBoundsY0
    title_y1 = title_y0 + title_height
    description_y0 = title_y1 + app.event_inner_padding
    description_y1 = description_y0 + description_height
    selector_y0 = description_y1 + app.event_inner_padding
    selector_y1 = selector_y0 + selector_height
    options_y0 = selector_y1 + app.event_inner_padding
    options_y1 = options_y0 + options_height
    save_y0 = options_y1 + app.event_inner_padding
    save_y1 = save_y0 + save_height
    if component == "title":
        return (layoutBoundsX0, title_y0, layoutBoundsX1, title_y1)
    elif component == "description":
        return (layoutBoundsX0, description_y0, layoutBoundsX1, description_y1)
    elif component == "selector":
        return (layoutBoundsX0, selector_y0, layoutBoundsX1, selector_y1)
    elif component == "options":
        return (layoutBoundsX0, options_y0, layoutBoundsX1, options_y1)
    elif component == "save":
        return (layoutBoundsX0, save_y0, layoutBoundsX1, save_y1)
    elif component == "whole":
        return (layoutBoundsX0, layoutBoundsX0, layoutBoundsX1, layoutBoundsY1)


def selector_panel_layout_manager(app, component):
    #layout manager for event type selector
    x0, y0, x1, y1 = create_event_layout_manager(app, "selector")
    paddingX = 30
    padding_middle = 10
    x0 += paddingX
    x1 -= paddingX
    width = x1 - x0
    total_length = width - padding_middle * 2
    btn_width = total_length / 3
    SE_x0 = x0
    SE_x1 = SE_x0 + btn_width
    RE_x0 = SE_x1 + padding_middle
    RE_x1 = RE_x0 + btn_width
    FE_x0 = RE_x1 + padding_middle
    FE_x1 = FE_x0 + btn_width
    if component == "SE":
        return (SE_x0, y0, SE_x1, y1)
    elif component == "RE":
        return (RE_x0, y0, RE_x1, y1) 
    elif component == "FE":
        return (FE_x0, y0, FE_x1, y1) 

def save_layout_manager(app, component):
    #layout manage for the bottom panel
    x0, y0, x1, y1 = create_event_layout_manager(app, "save")
    paddingX = 20
    x0 += paddingX
    x1 -= paddingX
    btn_length = 100
    if component == "save":
        return (x0, y0, x0 + btn_length, y1)
    elif component == "message":
        return (x0 + btn_length + paddingX, y0)

def get_button_x(x0, i, total_num, btn_length, padding, width):
    #returns the x coordinates for a button in a row of buttons
    middle_X = x0 + width //2 
    new_x0 = (middle_X - btn_length * (total_num / 2) - padding 
    + (btn_length + padding) * i)
    new_x1 = new_x0 + btn_length
    return new_x0, new_x1

def SE_layout_manager(app, component):
    #layout manager for strict events
    margin = 20
    x0, y0, x1, y1 = create_event_layout_manager(app, "options")
    x0 += margin
    x1 -= margin
    y0 += margin
    y1 -= margin
    height = y1 - y0
    width = x1 - x0
    date_height = height * 0.3
    time_height = height * 0.3
    time_title_height = height * 0.15
    d_y0 = y0
    d_y1 = d_y0 + date_height
    time_title_y0 = d_y1 + margin 
    time_title_y1 = time_title_y0 + time_title_height
    t_y0 = time_title_y1 + margin 
    t_y1 = t_y0 + time_height
    button1_length = width * 0.2
    time_button_length = width *.1
    if component == "Year":
        new_x0, new_x1 = get_button_x(x0, 0, 3, button1_length, 20, width)
        return new_x0, d_y0, new_x1, d_y1
    elif component == "Month":
        new_x0, new_x1 = get_button_x(x0, 1, 3, button1_length, 20, width)
        return new_x0, d_y0, new_x1, d_y1
    elif component == "Day":
        new_x0, new_x1 = get_button_x(x0, 2, 3, button1_length, 20, width)
        return new_x0, d_y0, new_x1, d_y1
    elif component == "Start_H":
        new_x0, new_x1 = get_button_x(x0, 0, 4, time_button_length, 30, width)
        return new_x0 - 30, t_y0, new_x1 - 30, t_y1
    elif component == "Start_M":
        new_x0, new_x1 = get_button_x(x0, 1, 4, time_button_length, 30, width)
        return new_x0 - 30, t_y0, new_x1 - 30, t_y1
    elif component == "End_H":
        new_x0, new_x1 = get_button_x(x0, 2, 4, time_button_length, 30, width)
        return new_x0 + 30, t_y0, new_x1 + 30, t_y1
    elif component == "End_M":
        new_x0, new_x1 = get_button_x(x0, 3, 4, time_button_length, 30, width)
        return new_x0 + 30, t_y0, new_x1 + 30, t_y1
    
def RE_and_FE_layout_manager(app, component):
    #layout manager for RE and FE components with the same placement
    margin = 10
    x0, y0, x1, y1 = create_event_layout_manager(app, "options")
    x0 += margin
    x1 -= margin
    y0 += margin
    y1 -= margin
    height = y1 - y0
    width = x1 - x0
    date_height = height * 0.2
    time_height = height * 0.2
    time_title_height = height * 0.15
    weekdays_height = height * 0.2
    d_y0 = y0
    d_y1 = d_y0 + date_height
    time_title_y0 = d_y1 + margin 
    time_title_y1 = time_title_y0 + time_title_height
    t_y0 = time_title_y1 + margin 
    t_y1 = t_y0 + time_height
    weekdays_y0 = t_y1 + margin + 20
    weekdays_y1 = weekdays_y0 + weekdays_height
    date_length = width *.1
    time_length = width * .1
    if component == "Year1":
        new_x0, new_x1 = get_button_x(x0, 0, 6, date_length, margin, width)
        return new_x0 - 50, d_y0, new_x1 - 50, d_y1
    elif component == "Month1":
        new_x0, new_x1 = get_button_x(x0, 1, 6, date_length, margin, width)
        return new_x0 - 50, d_y0, new_x1 - 50, d_y1
    elif component == "Day1":
        new_x0, new_x1 = get_button_x(x0, 2, 6, date_length, margin, width)
        return new_x0 - 50, d_y0, new_x1 - 50, d_y1
    elif component == "Year2":
        new_x0, new_x1 = get_button_x(x0, 3, 6, date_length, margin, width)
        return new_x0 + 50, d_y0, new_x1 + 50, d_y1
    elif component == "Month2":
        new_x0, new_x1 = get_button_x(x0, 4, 6, date_length, margin, width)
        return new_x0 + 50, d_y0, new_x1 + 50, d_y1
    elif component == "Day2":
        new_x0, new_x1 = get_button_x(x0, 5, 6, date_length, margin, width)
        return new_x0 + 50, d_y0, new_x1 + 50, d_y1
    elif component == "Start_H":
        new_x0, new_x1 = get_button_x(x0, 0, 4, time_length, 30, width)
        return new_x0 - 50, t_y0, new_x1 - 50, t_y1
    elif component == "Start_M":
        new_x0, new_x1 = get_button_x(x0, 1, 4, time_length, 30, width)
        return new_x0 - 50, t_y0, new_x1 - 50, t_y1
    elif component == "End_H":
        new_x0, new_x1 = get_button_x(x0, 2, 4, time_length, 30, width)
        return new_x0 + 50, t_y0, new_x1 + 50, t_y1
    elif component == "End_M":
        new_x0, new_x1 = get_button_x(x0, 3, 4, time_length, 30, width)
        return new_x0 + 50, t_y0, new_x1 + 50, t_y1
    elif component == "row_3_info":
        return width, margin, weekdays_y0, weekdays_y1, x0
    elif component == "row_2_info":
        return width, margin, t_y0, t_y1, x0, time_length

def RE_layout_manager(app, component):
    #RE specific buttons layout
    width, margin, weekdays_y0, weekdays_y1, x0 = RE_and_FE_layout_manager(app, "row_3_info")
    weekdays = ["sun", "mon", "tue", "wed", "th", "fri", "sat"]
    btn3_length = (width + margin * 6) / 12
    if component in weekdays:
        i = weekdays.index(component)
        new_x0, new_x1 = get_button_x(x0, i, 7, btn3_length, margin, width)
        return new_x0, weekdays_y0, new_x1, weekdays_y1

def FE_layout_manager(app, component):
    #FE specific buttons layout
    width, margin, weekdays_y0, weekdays_y1, x0 = RE_and_FE_layout_manager(app, "row_3_info")
    width, margin, t_y0, t_y1, x0, time_length = RE_and_FE_layout_manager(app, "row_2_info")
    length = width / 6
    num_x0 = x0 + width / 2 - length /2
    if component == "Num_Days":
        return num_x0, weekdays_y0, num_x0 + length, weekdays_y1
    elif component == "Start_H":
        new_x0, new_x1 = get_button_x(x0, 0, 2, time_length, margin, width)
        return new_x0 - 20, t_y0, new_x1 - 20, t_y1
    elif component == "Start_M":
        new_x0, new_x1 = get_button_x(x0, 1, 2, time_length, margin, width)
        return new_x0 + 20, t_y0, new_x1 + 20, t_y1