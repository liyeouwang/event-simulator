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
        self.new_task = False 
        self.max_tasks = 5
        self.decision = False

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

        # if there is a new task arrival, return event type: decision
        e = None
        if self.decision == True: #
            # check out the capacity itself
            # or maybe compare the priority with other tasks  
            if len(self.tasks) >= self.max_tasks:
                e = Event(name="Propagation", task=self.tasks[-1], server=self.server_id)
                self.tasks.pop()
                return e
            else:
                pass

            


        if self.new_task == True: #have_new_task 
            e = Event(name="Decision", task=self.tasks[-1], server=self.server_id)
            return e
                     

        # if there is no new task arrival, continue to do execution 
        if len(self.tasks) == 0:
            return Event("Idle")

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
            t = self.tasks.pop(0)
            e = Event(name="Delivery", task=t, info={"source":self.server_id, "dest": (self.server_id+1)%5})

        else:
            # Execution:
            self.tasks[0].just_do_it(1)
            e = Event(name="Execution", task=self.tasks[0])

        return e
    

    def add_task(self, task):
        self.tasks.append(task)
        return



    