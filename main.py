from cmu_112_graphics import *
from calendarHome import *
from calendarLayout import *
from date_functions import *
import datetime

# CITATION: screen structure from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

def calVariables(app):
    app.hours = ["12:00 A.M", "1:00 A.M.", "2:00 A.M.", "3:00 A.M", "4:00 A.M.", 
    "5:00 A.M.", "6:00 A.M", "7:00 A.M.", "8:00 A.M.", "9:00 A.M.", 
    "10:00 A.M.", "11:00 A.M.", "12:00 P.M", "1:00 P.M.", "2:00 P.M.", 
    "3:00 P.M", "4:00 P.M.", "5:00 P.M.", "6:00 P.M", "7:00 P.M.", "8:00 P.M.", 
    "9:00 P.M.", "10:00 P.M.", "11:00 P.M."]
    app.hoursViewed = 8
    app.cols = 7
    app.firstHour = 9
    app.firstWeekDay = calendar.SUNDAY
    app.lastHour = app.firstHour + app.hoursViewed
    app.shownHours = app.hours[app.firstHour:app.lastHour]
    app.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", 
    "Sept", "Oct", "Nov", "Dec"]
    app.weekdays = ["Sun", "Mon", "Tue", "Wed", "Th", "Fri", "Sat"]
    app.currentDate = get_current_date()
    app.yearRange = (2010, datetime.MAXYEAR)
    app.monthRange = (1, 12)
    app.currentWeek = get_week(app, app.currentDate.year, app.currentDate.month, 
    app.currentDate.day)

def calendarLayoutVariables(app):
    app.margin = 30
    app.layoutSpacing = 20
    app.calendarPadding = 20
    app.selector_padding = 30

    app.calOptions = [("Create Event", "eventsPage"), 
    ("See Today", "seeToday")]
    app.calOptionBtnObject = []
    calendar_option_btns(app, True)

    app.calSelects = [("year", app.currentDate.year), 
    ("month", app.currentDate.month), ("day", app.currentDate.day)]
    app.calSelectsOther = {"Left": "moveLeft", "Go": "chooseDate", 
    "Right": "moveRight"}
    app.calSelectorMoveBtns = []
    app.calSelectorInputs = []
    calendar_select_input(app, True)

def appStarted(app):
    #starts app
    app.mode = "calendarHome"
    app.calendarMode = "week" #options: week, month, year
    app.recentBtn = None
    reset_typing_setting(app)
    calVariables(app)
    calendarLayoutVariables(app)

runApp(width=500, height=800)