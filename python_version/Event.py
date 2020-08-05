from Task import Task

class Event:
    def __init__(self, name="", detail="No description."):
        self.name = name
        self.detail = detail
        return
        
    def __str__(self):
        return self.name + ": " + self.detail
        
