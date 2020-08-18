from Task import Task
from Event import Event

class Server:
    # All servers share tasks in all_tasks
    # Their own tasks are stored in all_tasks[server_id]
    # Let self.tasks = all_tasks[server_id]. Just use self.tasks, since this will make it more clear.
    all_tasks = [] 
    server_num = 0

    #new_tasks = []
    propagation_tasks = []

    def __init__(self, server_id):
        self.tasks = self.all_tasks[server_id] # a list of Task
        self.server_id = server_id
        self.have_new_task = False 
        self.max_tasks = 5
        #self.make_decision = False
        self.new_tasks = []
        self.propagation_tasks = self.propagation_tasks


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
        e_prop = None 
        if self.have_new_task == True: 
            # make decision (now only consider single task)
            e_prop = self.make_decision(self.new_tasks[0])

        # ====== execution part ======
        # continue to do execution 
        e_idle = None
        e_deli = None
        if len(self.tasks) == 0:
            e_idle = Event("Idle")               
        elif self.tasks[0].is_done():
            # Delivery
            t = self.tasks.pop(0)
            e_deli = Event(name="Delivery", task=t, server_id=self.server_id)
        else:
            # Execution:
            self.tasks[0].just_do_it(1)
            #e = Event(name="Execution", task=self.tasks[0]) 

        if e_prop != None:
            return e_prop
        elif e_deli != None:
            return e_deli
        else:
            return e_idle
    

    def add_task(self, task):
        self.new_tasks.append(task)
        return


    def make_decision(self, task):
        if len(self.tasks) >= self.max_tasks:
            #add a propagation flag in?
            #add to propagation list 
            self.propagation_tasks.append(tasks)
            self.new_tasks.pop()
            return Event(name="Propagation", task=task, server_id=self.server_id)

        else:
            self.tasks.append(task)
            self.new_tasks.pop()
            return None 

    