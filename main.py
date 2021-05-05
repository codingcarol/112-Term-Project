from cmu_112_graphics import *
from calendarHome import *
from date_functions import *
import datetime
from event_functions import *
from flex_event_functions import *
from create_event_home import * 
from overall_scheduling import *
from report_home import *
# CITATION: screen structure from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

def calVariables(app):
    #initialize calendar variables
    app.hours = ["12:00 A.M.", "1:00 A.M.", "2:00 A.M.", "3:00 A.M", "4:00 A.M.", 
    "5:00 A.M.", "6:00 A.M.", "7:00 A.M.", "8:00 A.M.", "9:00 A.M.", 
    "10:00 A.M.", "11:00 A.M.", "12:00 P.M", "1:00 P.M.", "2:00 P.M.", 
    "3:00 P.M", "4:00 P.M.", "5:00 P.M.", "6:00 P.M.", "7:00 P.M.", "8:00 P.M.", 
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
    app.currentDate = date.fromisoformat('2021-04-18') #get_current_date()
    app.yearRange = (datetime.MINYEAR, datetime.MAXYEAR)
    app.monthRange = (1, 12)
    app.currentWeek = get_week(app, app.currentDate.year, app.currentDate.month, 
    app.currentDate.day) 

def calendarLayoutVariables(app):
    #initialize calendar layout variables
    app.margin = 30
    app.layoutSpacing = 20
    app.calendarPadding = 20
    app.selector_padding = 30
    
    app.calOptions = [("Create Event", "createEvent"), 
    ("See Today", "seeToday"), ("Flex Schedule", "flexSchedule"), 
    ("Report", "report")]
    app.calOptionBtnObject = []
    calendar_option_btns(app, True)

    app.calSelects = [("year", app.currentDate.year), 
    ("month", app.currentDate.month), ("day", app.currentDate.day)]
    app.calSelectsOther = {"Left": "moveLeft", "Go": "chooseDate", 
    "Right": "moveRight"}
    app.calSelectorMoveBtns = []
    app.calSelectorInputs = []
    calendar_select_input(app, True)

def create_event_variables(app):
    #initialize create event variables
    app.event_paddingX = 100
    app.event_paddingY = 50
    app.event_inner_padding = 10

    app.event_title = ("Create Title", "title")
    app.event_description = ("Description", "")
    app.event_types_btns = [("Strict", "SE"), ("Recurring Strict", "RE"), ("Flexible", "FE")]
    app.event_save_btn = ("Save", "Save")
    app.event_always_btns = {'title': '', 'description': '', 'RE': '', "SE": '', "FE": '',
    "save": ''}
    app.just_resized = False
    app.current_event_panel = "SE"
    
    app.event_date1 = [("Year1", app.currentDate.year), 
    ("Month1",  app.currentDate.month), ("Day1", app.currentDate.day)]
    app.event_date2 = [("Year2", app.currentDate.year), 
    ("Month2", app.currentDate.month), ("Day2", app.currentDate.day)]
    app.event_start_t_h = ("Start Time H", "start_t_h")
    app.event_end_t_h = ("End Time H", "end_t_h")
    app.event_start_t_m = ("Start Time M", "start_t_m")
    app.event_end_t_m = ("End Time M", "end_t_m")
    app.event_weekday_btns = (('S', "sun"), ('M', "mon"), ('T', "tue"), 
    ("W", "wed"), ("TH", "th"), ("F", "fri"), ("S", "sat"))
    app.event_num_days = ("Num Days", "num_days")
    app.SE_btns = {'Year': '', 'Month': '', "Day": '', "Start_H": '', "End_H": '',
    "Start_M": '', "End_M": ''}
    app.FE_btns = {'Year1': '', 'Month1': '', "Day1": '', 'Year2': '', 
    'Month2': '', "Day2": '', "Start_H": '', "Start_M": '', 'Num_Days': ''}
    app.RE_btns = {'Year1': '', 'Month1': '', "Day1": '', 'Year2': '', 
    'Month2': '', "Day2": '', "Start_H": '', "End_H": '', 'Week_Days': {}, 
    "Start_M": '', "End_M": ''}
    create_event_input(app)

def record_vars(app):
    #initialize record event variables
    app.record_btns = {'title': '', 'year': '', 'month': '', 'day': '', 'start_t_H': '',
    'start_t_M':'', 'missed': '', 'mood': '', 'save': ''}
    create_record_input(app)

def appStarted(app):
    #starts app and initialize variables
    app.mode = "calendarHome" #options: calendarHome, createEvent, report
    app.calendarMode = "week"
    app.recentBtn = None
    app.schedule_folder = "sample_schedule1"
    reset_typing_setting(app)
    calVariables(app)
    calendarLayoutVariables(app)
    create_event_variables(app)
    record_vars(app)
    app.schedule = construct_strict_schedule(app)

runApp(width=1000, height=800)