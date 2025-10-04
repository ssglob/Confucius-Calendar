from datetime import datetime
from pathlib import Path
from Task_Scheduler import _d

def create_task():
    task = input("Enter the task: ")
    date = input("Enter datetime: ")
    parsed_date = _d(date)

    duration = ""
    while not duration.isdigit():
        duration = input("Enter how long this task will take (hours): ")
    duration = int(duration)

    new_task = {"task": task, "date": parsed_date, "duration": duration}
    return new_task


def update_task(task):
    task.date

def print_tasks(tl):
    if (len(tl) == 0):
        print("You have no tasks")
        return
    for i in range(len(tl)):
        print(f"{i + 1}.\ttask: {tl[i]["task"]}\n\tdate: {tl[i]["date"]}\n\tduration: {tl[i]["duration"]}")

def serialize(tl):
    for i in tl:
        i["date"] = i["date"].strftime("%d-%m-%Y")