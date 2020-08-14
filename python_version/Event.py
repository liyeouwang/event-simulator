from Task import Task

class Event:
    def __init__(self, name="", task=None, detail="No description.", info={}, server_id=0):
        self.name = name # Delivery, Execution, Propagation
        self.detail = detail
        self.task = task 
        self.info = info # fill in anything you want
        self.server_id = server_id # the server that this event belongs to 
        return
        
    def __str__(self):
        s = ""
        s += self.name
        s += (' ' + str(self.task))
        return s

    def get_task(self):
        return self.task
        
