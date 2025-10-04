class Task:
    def __init__(self, task, date, duration):
        self.task = task
        self.date = date
        self.duration = duration        

    def update(self, dictionary):
        if dictionary["task"]:
            self.task = dictionary["task"]
        
        if dictionary["date"]:
            self.date = dictionary["date"]

        if dictionary["duration"]:
            self.duration = dictionary["duration"]
    