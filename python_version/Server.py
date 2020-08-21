from Task import Task
from Event import Event

class Server:
    # All servers share tasks in all_tasks
    # Their own tasks are stored in all_tasks[server_id]
    # Let self.tasks = all_tasks[server_id]. Just use self.tasks, since this will make it more clear.
    all_tasks = [] 
    server_num = 0

    all_new_tasks = []
    all_propagation_tasks = []
    time_slot = 0

    def __init__(self, server_id):
        self.tasks = self.all_tasks[server_id] # a list of Task
        self.server_id = server_id
        self.max_tasks = 5
        #self.make_decision = False
        self.new_tasks = self.all_new_tasks[server_id]
        self.propagation_tasks = self.all_propagation_tasks[server_id]
        self.status = {
            'state': 'IDLE',
            'task': None,
        }


    def event_handler(self, event):
        # Handle the event. Maybe add tasks to taskQueue? Or anything...
        pass

    def insert_task(self, task):
        self.tasks.append(task)
        return

    def __str__(self):
        s = '\n*************************\n'
        s += 'Status: ' + self.status['state']
        if self.status['state'] != 'IDLE':
            s += str(self.status['task'].task_id)
        s += '\n-------Task queue-------\n'
        for task in self.tasks:
            s += str(task) + '\n'

        s += '--------New task--------\n'
        for t in self.new_tasks:
            s += str(t) + '\n'

        s += '----Propagation task----\n'
        for t in self.propagation_tasks:
            s += str(t) + '\n'

        s += '*************************\n'

        return s
    
    def run(self):
        # ====== TODO =======
        # This part of code should decide how to deal with the task queue.
        # Execution, Propagation, Delivery... or 
        # or spend some times on deciding like checking priority? 
        # Ex: "Execution. task_info"
        # Ex: Propagation. to which server? what task?
        # Ex: Delivery...

        # 1. deal with propagation list (simulator do it?)
        # 2. check if there is new task arrival. 
        # 3. If there is new task arrival, make decision. (append to propagation list or remain in task list)
        # 4. executing tasks 
        # 5. return event 
      
        # ====== decision part (propagate or add to task queue) ======
        while len(self.new_tasks):
            # make decision 
            self.make_decision(self.new_tasks[0])

        # ====== propagation buffer ======
        e_prop = None 
        if len(self.propagation_tasks) != 0:
            t = self.propagation_tasks[0]
            e_prop = Event(name="Propagation", task=t, server_id=self.server_id)
            self.propagation_tasks.pop(0)

        # ====== execution part ======
        # continue to do execution 
        if len(self.tasks) == 0:
            self.status['state'] = 'IDLE'
            self.status['task'] = None
        elif self.tasks[0].is_done():
            # Delivery
            t = self.tasks.pop(0)
            # e_deli = Event(name="Delivery", task=t, server_id=self.server_id)
            self.status['state'] = 'Delivery'
            self.status['task'] = t

        else:
            # Execution:
            self.tasks[0].just_do_it(1)
            # e = Event(name="Execution", task=self.tasks[0], server_id=self.server_id) 
            self.status['state'] = 'Execution'
            self.status['task'] = self.tasks[0]

        return e_prop
    
    def add_task(self, task):
        self.new_tasks.append(task)
        return

    def make_decision(self, task):
        if len(self.tasks) >= self.max_tasks:
            self.propagation_tasks.append(task)
            self.new_tasks.pop(0)
        else:
            self.tasks.append(task)
            self.new_tasks.pop(0)

    def get_status(self):
        return self.status
    



