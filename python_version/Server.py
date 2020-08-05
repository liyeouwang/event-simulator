from Task import Task
from Event import Event

class Server:
    # All servers share tasks in all_tasks
    # Their own tasks are stored in all_tasks[server_id]
    # Let self.tasks = all_tasks[server_id]. Just use self.tasks, since this will make it more clear.
    all_tasks = [] 
    server_sum = 0

    def __init__(self, server_id):
        self.tasks = self.all_tasks[server_id] # a list of Task
        self.server_id = server_id

    def event_handler(self, event):
        # Handle the event. Maybe add tasks to taskQueue? Or anything...
        pass

    def insert_task(self, task):
        self.tasks.append(task)
        return

    def __str__(self):
        s = ''
        s += 'Task queue\n'
        for task in self.tasks:
            s += str(task) + '\n'
        return s
    
    def run(self):
        if len(self.tasks) == 0:
            return Event("Idle", "Do nothing.")

        # ====== TODO =======
        # This part of code should decide how to deal with the task queue.
        # Execution, Propagation, Delivery... or 
        # or spend some times on deciding like checking priority? 
        # Ex: "Execution. task_info"
        # Ex: Propagation. to which server? what task?
        # Ex: Delivery...
        
        e = None
        if self.tasks[0].is_done():
            # Delivery
            t = self.tasks.pop()
            e = Event("Delivery: " + str(t))
        else:
            # Execution:
            self.tasks[0].just_do_it(1)
            e = Event("Execution: " + str(self.tasks[0]))


        return e
    

    def add_task(self, task):
        self.tasks.append(task)
        return
    