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
    tasklist.sort(key = lambda t: _d(t.date))
    return tasklist

def refresh_list(tasklist: list, updated_task) -> list:
    """
    call after changed fields on task object
    task.update(date = '')
    resorted by due date and returned list
"""
    tasklist.sort(key = lambda t: _d(t.date))
    return tasklist
# LLM stuff