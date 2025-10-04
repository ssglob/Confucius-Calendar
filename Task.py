class Task:
    def __init__(self, task, date, duration):
        self.task_data = {"task": task, "date": date, "duration": duration}

    def update(self, dictionary):
        self.task_data = dictionary