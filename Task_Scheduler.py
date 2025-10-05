from datetime import datetime
Date_fmt = "%d-%m-%Y"

def _d(s: str) -> datetime:
    #date string to datetime for sorting
    return datetime.strptime(s, Date_fmt)

def insert_task(tasklist: list, task) -> list:
    """
    tasklist: list[Task]
    task:  from task.py
    1) add to list
    2) sort by earliest due date
    3) return the same (sorted) list
    """
    tasklist.append(task)
    tasklist.sort(key = lambda t: t["date"])
    return tasklist

def refresh_list(tasklist: list, updated_task) -> list:
    """
    call after changed fields on task object
    task.update(date = '')
    resorted by due date and returned list
"""
    tasklist.sort(key = lambda t: t["date"])
    return tasklist

import json
from gen_ai import generate_schedule

def schedule_tasks(tasklist: list, schedule_file_path: str):
    """Generates a schedule using AI and saves it to a file."""
    print("Generating schedule with AI...")
    schedule_response = generate_schedule(tasklist)
    
    try:
        # Find the start and end of the JSON block
        json_start = schedule_response.find('{')
        json_end = schedule_response.rfind('}') + 1
        
        if json_start != -1 and json_end != 0:
            schedule_json = schedule_response[json_start:json_end]
            schedule = json.loads(schedule_json)
            with open(schedule_file_path, "w") as f:
                json.dump(schedule, f, indent=4)
            print("Schedule generated and saved to data/schedule.json")
        else:
            print("Error: Could not find a valid JSON block in the AI's response.")
            print("Raw response:", schedule_response)

    except json.JSONDecodeError:
        print("Error: Could not decode the schedule from the AI.")
        print("Raw response:", schedule_response)

# LLM stuff