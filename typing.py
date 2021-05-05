from cmu_112_graphics import *

def reset_typing_setting(app):
    #resets the typing variables
    app.typing = False
    app.typed_word = ""
    app.text_box = None

def typing_event(app, event):
    if event.key == "Delete" and len(app.typed_word) > 0: #delete word w backspace
        app.typed_word = app.typed_word[:-1]
    elif app.text_box.get_valid_characters() != True: #do not type letter if not valid
        if event.key in app.text_box.get_valid_characters():
            app.typed_word += event.key
    else: #otherwise, tupe word
        app.typed_word += event.key
    if ("month" in app.text_box.name.lower() or 
    "day" in app.text_box.name.lower() or "start" in app.text_box.name.lower()
    or "end" in app.text_box.name.lower() or "mood" in app.text_box.name.lower()):
        #types of buttons that can only have 2 characters
        app.typed_word = app.typed_word[:2]
    if "year" in app.text_box.name.lower(): #only 4 characters
        app.typed_word = app.typed_word[:4]
    if ("missed" in app.text_box.name.lower() or "num_days" in app.text_box.name.lower()):
        #only 1 character 
        app.typed_word = app.typed_word[:1]
    if "title" in app.text_box.name.lower(): #makes sure title text doesn't go over button
        if event.key == "Space":
            app.typed_word += " "
        x0, y0, x1, y1 = app.event_always_btns['title'].get_coord()
        width = x1 - x0
        max_letters = width // 10
        app.typed_word = app.typed_word[:max_letters]
    elif app.text_box.name == "Description": #makes sure description text doesn't go over button
        #also makes sure that a new line is created when text reaches max line limit
        if event.key == "Space":
            app.typed_word += " "
        x0, y0, x1, y1 = app.event_always_btns['description'].get_coord()
        max_lines = 5
        width = x1 - x0
        max_letters = width // 8
        lines = 1
        letters = ""
        line_let_count = 0
        for i in range(len(app.typed_word)):
            if app.typed_word[i] != '\n':
                line_let_count += 1
                if line_let_count == max_letters and lines < max_lines:
                    letters += "\n"
                    lines += 1
                    line_let_count = 0
                letters += app.typed_word[i]
                if line_let_count == max_letters and lines == max_lines:
                    break
        app.typed_word = letters
    app.text_box.set_value(app.typed_word)