from cmu_112_graphics import *
from calendarHome import *
from calendarLayout import *
# CITATION: screen structure from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

def calVariables(app):
    app.hours = ["12:00 A.M", "1:00 A.M.", "2:00 A.M.", "3:00 A.M", "4:00 A.M.", 
    "5:00 A.M.", "6:00 A.M", "7:00 A.M.", "8:00 A.M.", "9:00 A.M.", 
    "10:00 A.M.", "11:00 A.M.", "12:00 P.M", "1:00 P.M.", "2:00 P.M.", 
    "3:00 P.M", "4:00 P.M.", "5:00 P.M.", "6:00 P.M", "7:00 P.M.", "8:00 P.M.", 
    "9:00 P.M.", "10:00 P.M.", "11:00 P.M."]
    app.hoursViewed = 9
    app.cols = 7
    app.firstHour = 8
    app.lastHour = app.firstHour + app.hoursViewed
    app.shownHours = app.hours[app.firstHour:app.lastHour]
    app.months = ["Jan", "Feb", "Mar"]
    app.currentDate = {"Year": 2021, "Month": 2, "Day": 1}
    app.currentWeek = [("Sun", 0), ("Mon", 1), ("Tue", 2), ("Wed", 3),
    ("Th", 4), ("Fri", 5), ("Sat", 6)]

def calendarLayoutVariables(app):
    app.margin = 30
    app.layoutSpacing = 20
    app.calendarPadding = 20
    app.calOptions = [("Create Event", "eventsPage"), 
    ("Button2", "Button2Redirect")]
    app.calOptionBtnObject = []
    calendar_option_btns(app, True)
    app.calSelects = [("Year", app.currentDate["Year"]), 
    ("Month", app.currentDate["Month"]), ("Day", app.currentDate["Day"])]
    app.calSelectsOther = [("Left", "moveLeft"), ("Go", "chooseDate"), 
    ("Right", "moveRight")]
    app.calSelectorInputs = []

def appStarted(app):
    #starts app
    app.mode = "calendarHome"
    app.calendarMode = "week" #options: week, month, year
    calVariables(app)
    calendarLayoutVariables(app)

runApp(width=1200, height=800)