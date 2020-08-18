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

        # Build servers 
        self.servers = [Server(i) for i in range(self.server_num)]


        self.events = [] # events of each server in time slot
        self.tasks = []
        self.time_slot = 1
        self.data_of_slot = []
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
        if len(self.events) > 0: 
            # prevent the empty events in the beginning
            print('Events:')
            for i, e in enumerate(self.events[-1]):
                print('Server ' + str(i) + ': ' + str(e))
        print("============================\n\n")
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
            recent_events.append(e)
        
        self.run_sync(recent_events)

        self.record(recent_events)
        self.random_insert_task()
        self.time_slot += 1
        # self.show_status()

    
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
    
    def record(self, recent_events):
        # add the info into history
        self.events.append(recent_events)
        self.data_of_slot.append({
            'unfinished_task_num': len(self.tasks) - self.finished_task_num,
        })
        return


    # not done    
    def event_dealer(self, event):

        # deal with propagation list
        if event == None:
            return
        if event.name == "Propagation":
            for task in self.servers[event.server_id].propagation_tasks:
                self.assign_task((event.server_id + 1) % self.server_num, event.get_task())
  
        if event.name == "Delivery":
            t = event.get_task()
            t.deliver(self.time_slot)
            self.finished_task_num += 1
        elif event.name == "Decision":
            self.servers[event.server_id].decision = True
        elif event.name == "Propagation":
            # propagation 
            # propagate the task to next server 
            self.assign_task((event.server_id + 1) % self.server_num, event.get_task())
        else:
            #if it is execution, do nothing 
            #scheduling is server's job
            pass
        return

    def assign_task(self, server_id, task):
        self.servers[server_id].add_task(task)
        self.servers[server_id].have_new_task = True
        return

    def create_task(self, name="", duration=1, have_done=0, 
                priority=0, request_time=0, detail="No task description"):
        # use this method to create task
        # so that we can make sure the created tasks are always added to the list.
        t = Task(name=name, duration=duration, have_done=have_done, 
                priority=priority, request_time=request_time, detail=detail)
        self.tasks.append(t)
        return t

    def random_insert_task(self):
        tasks_config = self.config["tasks_config"]
        for i in range(self.server_num):
            for task_config in tasks_config:
                if uniform(0, 1) < task_config["occur_probability"]:
                    t = self.create_task(name=task_config["name"],
                            duration=randint(task_config["duration_range"][0], task_config["duration_range"][1]),
                            priority=task_config["priority"], request_time=self.time_slot) 
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
        for i, event in enumerate(self.events):
            for e in event:
                brief_events.append({
                    'time_slot': i,
                    'server_id': e.server_id,
                    'name': e.name
                })

        data = {
            'finished_task': finished_tasks,
            'events': brief_events,
            'data_of_slot': self.data_of_slot
        }

        return data


    