class Task:
    def __init__(self, task, date, duration):
        self.task = task
        self.date = date
        self.duration = duration        

    def update(self, task, dictionary):
        if dictionary["task"]:
            self.task = task.task
        
        if dictionary["date"]:
            self.date = task.date

        if dictionary["duration"]:
            self.duration = task.duration
    