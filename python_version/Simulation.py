import os
import sys
from random import randint, choice, uniform
sys.path.append(".")
from Task import Task
from Event import Event
from Server import Server

class Simulator:
    def __init__(self, config):
        self.config = config
        self.server_num = config["server_num"]

        # initialize class attribute of Server
        Server.server_num = self.server_num
        Server.all_tasks = [[] for i in range(self.server_num)]
        Server.all_propagation_tasks = [[] for i in range(self.server_num)]
        Server.all_new_tasks = [[] for i in range(self.server_num)]

        # Build servers 
        self.servers = [Server(i) for i in range(self.server_num)]

        self.events = [] # events of each server in time slot
        self.tasks = []
        self.time_slot = 1
        self.data_of_slot = {
            'unfinished_task_num': [],
            'server_loading_task': [],
            'server_loading_new_task': []
        }
        self.finished_task_num = 0


    def __str__(self):
        s = ''
        s += 'Number of servers: {}\n'.format(len(self.servers))
        for i in range(len(self.servers)):
            s += 'Server {}: {}\n'.format(i, str(self.servers[i]))
        return s

    def add_tasks_to_servers(self, data):
        # data format: [(server_id, Task)]
        for task in data:
            self.tasks.append(task[1])
            self.assign_task(task[0], task[1])
        return
        # for task in self.all_tasks:
        #     self.servers[task[0]].add_task(task[1])
        # return

    def show_status(self):
        # print out current status
        # including: 
        # All Server status
        # What round is this?

        print("======= Time Slot " + str(self.time_slot) + " =======")
        print(self)
        
        return
    

    def get_task_waiting_time(self, name=None):
        waiting_time = [t.get_waiting_time() if t.is_delivered() else None for t in self.tasks]
        return waiting_time

    def run(self, round=15):

        while True:
            if self.time_slot > round:
                break
            self.run_one()
    
    def run_one(self):
        # Run the simulation. Can be a while loop?
        # run all server 
        # and then run synchronization
        recent_events = []
        for i in range(self.server_num):
            e = self.run_server(i)
            # print('Server ' + str(i) + ': ' + str(e))
            if e != None:
                recent_events.append(e)
        
        self.run_sync(recent_events)

        self.record(recent_events)
        self.random_insert_task()

        self.time_slot += 1
        Server.time_slot += 1
        # self.show_status()

        # This can show each round task queue.
        # Provide quite good view of what's going on.
        print('finished task:', self.finished_task_num, 'all tasks:', len(self.tasks))

        print([len(s.tasks) for s in self.servers])
        print([len(s.propagation_tasks) for s in self.servers])
        print([len(s.new_tasks) for s in self.servers])

    
    def run_server(self, server_id):
        # Time to run this server
        # get event from server
        event = self.servers[server_id].run()
        return event
    
    def run_sync(self, events):
        # already get all events from servers in this round
        # pass them to corresponding server
        for event in events:
            self.event_dealer(event)
        
        # Scan the status of all servers
        for s in self.servers:
            status = s.get_status()
            if status['state'] == 'Delivery':
                status['task'].deliver(self.time_slot)
                self.finished_task_num += 1
    

    # not done    
    def event_dealer(self, event):

        #TODO 2020/08/21
        # This event dealer should only take care of Propogation. (at least so far)

        # deal with propagation list
        if event == None:
            return
        elif event.name == "Propagation":
            self.assign_task((event.server_id + 1) % self.server_num, event.get_task())
  
        # elif event.name == "Delivery":
        #     t = event.get_task()
        #     t.deliver(self.time_slot)
        #     self.finished_task_num += 1
        else:
            #if it is execution, do nothing 
            #scheduling is server's job
            pass
        return

    def record(self, recent_events):
        # add the info into history
        self.events.extend(recent_events)
        self.data_of_slot['unfinished_task_num'].append(len(self.tasks) - self.finished_task_num)
        self.data_of_slot['server_loading_task'].append([len(s.tasks) for s in self.servers])
        self.data_of_slot['server_loading_new_task'].append([len(s.new_tasks) for s in self.servers])

        return



    def assign_task(self, server_id, task):
        self.servers[server_id].add_task(task)
        return

    def create_task(self, name="", duration=1, have_done=0, 
                priority=0, request_time=0, detail="No task description", task_id=0):
        # use this method to create task
        # so that we can make sure the created tasks are always added to the list.
        t = Task(name=name, duration=duration, have_done=have_done, 
                priority=priority, request_time=request_time, detail=detail, task_id=task_id)
        self.tasks.append(t)
        return t

    def random_insert_task(self):
        tasks_config = self.config["tasks_config"]
        for i in range(self.server_num):
            if i % 2 == 0:
                continue
            for task_config in tasks_config:
                if uniform(0, 1) < task_config["occur_probability"]:
                    t = self.create_task(name=task_config["name"],
                            duration=randint(task_config["duration_range"][0], task_config["duration_range"][1]),
                            priority=task_config["priority"], request_time=self.time_slot, task_id=len(self.tasks)) 
                    self.assign_task(i, t)

        return

    def get_pack_data(self):
        data = {
            'server_num': self.server_num,
            'tasks': [t.__dict__ for t in self.tasks],
            'events': [[e.__dict__ for e in event] for event in self.events]
        }
        return data

    def get_evaluation_data(self):
        # Prun task data
        finished_tasks = []
        for t in self.tasks:
            if t.is_delivered():
                finished_tasks.append({
                    'name': t.name,
                    'waiting_time': t.get_waiting_time(),
                    'priority': t.priority,
                    'duration': t.duration
                })

        # Prun event data
        brief_events = []
        for e in self.events:
            brief_events.append({
                'server_id': e.server_id,
                'name': e.name
            })

        data = {
            # 'finished_task': finished_tasks,
            # 'events': brief_events,
            'data_of_slot': self.data_of_slot
        }

        return data


    