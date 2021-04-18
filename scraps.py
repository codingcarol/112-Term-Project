from cmu_112_graphics import *
import random

def appStarted(app):
    app.scrollX = 0

def keyPressed(app, event):
    if (event.key == "Left"):    app.scrollX -= 5
    elif (event.key == "Right"): app.scrollX += 5

def redrawAll(app, canvas):
    canvas.create_rectangle(100, 100, 200, 200, fill="pink")
    canvas.create_oval(120, 90, 130, 100, fill="blue")
    canvas.create_oval(150, 150, 160, 160, fill="red")
    canvas.create_oval(150, 230, 160, 240, fill="green")

runApp(width=300, height=300)