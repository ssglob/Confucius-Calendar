from Task import Task
from datetime import datetime
from pathlib import Path

def parse_date(string, time):
    numbers = "0123456789"
    s = string.split("/")
    day, month, year = 0, 0, 0
    hour, minute = 0, 0
    if len(s) < 3:
        return None
    
    for item in range(len(s)):
        if item in [0, 1] and len(s[item]) != 2:
            return None
        if item == 2 and len(s[item]) != 4:
            return None
        
        if not s[item].is_digit():
            return None

        if item == 0:
            day = int(s[item])
        if item == 1:
            month = int(item)
        if item == 2:
            year = int(item)
    
    try:
        return datetime(year, month, day, time)
    except:
        return None

def add_task():
    task = input("Enter the task.")
    parsed_date = None
    while not parsed_date:
        date = input("Enter the date you must finish this task")
        time = input("Enter the time that you must finish this task (HH:MM)")
        duration = input("Enter how long this task will take")
        duration = int(duration)

        parsed_date = parse_date(date, int(time))

    new_task = Task(task)