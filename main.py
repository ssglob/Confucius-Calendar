from Task import Task
import json
from datetime import datetime
from pathlib import Path
from handle_task import create_task
from Task_Scheduler import insert_task

def main():
    dir = Path('.')
    p = dir / "data" / "tasklist.json"
    if not p.exists():
        p.write_text("[]", encoding="utf-8")

    try:
        with p.open("r") as f:
            tasklist = json.load(f)
    except:
        tasklist = []

    action = input("What would you like to do to the task list? Enter the corresponding number.\n"+
                   "1. Add a task\n" +
                   "2. Update an existing task\n")
    
    action = int(action)

    if action == 1:
        new_task = create_task()
        insert_task(tasklist, new_task)
        
    with p.open("w") as f:
        json.dump(tasklist, f)

main()