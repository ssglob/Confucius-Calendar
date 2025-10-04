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

    new_task = {"task": task, "date": date, "duration": duration}
    return new_task


def update_task(task):
    print("Current task details:")
    print(f"1. Task name: {task['task']}")
    print(f"2. Date: {task['date']}")
    print(f"3. Duration: {task['duration']} hours")
    print("Which field do you want to update?")
    print("Enter the number (1 for name, 2 for date, 3 for duration), or press Enter to skip.")

    # Update task name
    choice = input("Field to update (1/2/3, or Enter to skip): ").strip()
    if choice == "1":
        new_name = input("Enter new task name: ")
        if new_name:
            task["task"] = new_name

    # Update date
    if choice == "2":
        new_date = input("Enter new date (dd-mm-yyyy): ")
        try:
            _d(new_date)  # Validate date format
            task["date"] = new_date
        except Exception:
            print("Invalid date format. Skipping date update.")

    # Update duration
    if choice == "3":
        new_duration = input("Enter new duration (hours): ")
        if new_duration.isdigit():
            task["duration"] = int(new_duration)
        else:
            print("Invalid duration. Skipping duration update.")
    else:
        print("Inavlid choice. No updates made.")
        
    return task

def print_tasks(tl):
    pass