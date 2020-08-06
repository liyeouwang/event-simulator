from Task import Task

class Event:
    def __init__(self, name="", task=None, detail="No description.", info={}):
        self.name = name # Delivery, Execution, Propagation
        self.detail = detail
        self.task = task 
        self.info = info # fill in anything you want
        return
        
    def __str__(self):
        s = ""
        s += self.name
        s += (' ' + str(self.task))
        return s
        
