from Task import Task
from datetime import datetime
from pathlib import Path
from Task_Scheduler import _d

def create_task():
    task = input("Enter the task.")
    date = input("Enter datetime")
    parsed_date = _d(date)

    duration = ""
    while not duration.isdigit():
        duration = input("Enter how long this task will take")
    duration = int(duration)

    new_task = Task(task, parsed_date, duration)

    new_task = Task(task)


def update_task(task):
    task.date