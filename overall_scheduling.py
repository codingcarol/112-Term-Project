import csv
from event_functions import *
from flex_event_functions import *
from datetime import date

def get_weekly_schedule(app, folder, week):
    #returns the weekly flexible schedule
    return generate_flexible_schedule(folder, construct_strict_schedule(app), week)