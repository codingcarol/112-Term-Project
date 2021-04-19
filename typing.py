from cmu_112_graphics import *

def reset_typing_setting(app):
    app.typing = False
    app.typed_word = ""
    app.text_box = None

def typing_event(app, event):
    if event.key == "Delete" and len(app.typed_word) > 0:
        app.typed_word = app.typed_word[:-1]
    elif (app.text_box.get_valid_characters() != True and
    event.key in app.text_box.get_valid_characters()):
        app.typed_word += event.key
    if app.text_box.name == "month" or app.text_box.name == "day":
        app.typed_word = app.typed_word[:2]
    if app.text_box.name == "year":
        app.typed_word = app.typed_word[:4]
    app.text_box.set_value(app.typed_word)