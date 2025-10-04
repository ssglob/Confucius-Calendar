import json
from datetime import datetime
from pathlib import Path
from handle_task import create_task, update_task, serialize, print_tasks
import Task_Scheduler

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
    
    for i in tasklist:
        i["date"] = Task_Scheduler._d(i["date"])

    action = input("What would you like to do to the task list? Enter the corresponding number.\n" +
                   "1. Add a task\n" +
                   "2. Update an existing task\n" +
                   "3. Print tasks\n" +
                   "4. Remove a task")
    
    action = int(action)

    if action == 1:
        new_task = create_task()
        Task_Scheduler.insert_task(tasklist, new_task)
        
    elif action == 2:
        task = input("Enter task id: ")
        task = tasklist[int(task)-1]
        update_task(task)
    
    elif action == 3:
        print_tasks(tasklist)
    
    elif action == 4:
        task = input("Enter task id: ")
        task = int(task) - 1
        del tasklist[task]

    serialize(tasklist)

    with p.open("w") as f:
        json.dump(tasklist, f)

main()