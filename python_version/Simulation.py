import os
import sys
from random import randint, choice, uniform
sys.path.append(".")
from Task import Task
from Event import Event
from Server import Server
from Vehicle import Vehicle

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
        self.servers = [Server(i, self.config["server_max_task"]) for i in range(self.server_num)]

        # Let's have some vehicles!
        self.vehicles = [Vehicle(i) for i in range(self.config["vehicle_num"])]
        Vehicle.config = self.config

        self.events = [] # events of each server in time slot
        self.tasks = []
        self.time_slot = 0
        self.data_wanted = config['data_wanted']
        self.data = {}
        self.init_data()

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

    def show_status(self):
        print("======= Time Slot " + str(self.time_slot) + " =======")
        print(self)   
        return

    def show_server_status(self):
        s = ''
        s += 'Number of servers: {}\n'.format(len(self.servers))
        for i in range(len(self.servers)):
            s += 'Server {}: {}\n'.format(i, str(self.servers[i]))
        print(s)

    def show_vehicle_status(self):
        s = ''
        s += 'Number of vehicle: {}\n'.format(len(self.vehicles))
        for i in range(len(self.vehicles)):
            s += str(self.vehicles[i])
        print(s)

    def get_task_waiting_time(self, name=None):
        waiting_time = [t.get_waiting_time() if t.is_delivered() else None for t in self.tasks]
        return waiting_time

    def run(self, round=15):
        while True:
            if self.time_slot > round:
                break
            self.run_one()
    
    def run_one(self):
        # Run servers
        recent_events = []
        for s in self.servers:
            e = s.run()
            if e != None:
                recent_events.append(e)

        # Run vehicles
        new_tasks = []
        for v in self.vehicles:
            t = v.run()
            if t != None:
                new_tasks.append(t)
        
        self.deal_with_servers(recent_events)
        self.deal_with_vehicles(new_tasks)

        if self.time_slot % self.config['data_collection_interval'] == 0:
            self.record_data(recent_events)
        # self.random_insert_task()

        self.time_slot += 1
        Server.time_slot += 1
        Vehicle.time_slot += 1
        self.show_status()

    def deal_with_servers(self, events):
        # already get all events from servers in this round
        # pass them to corresponding server
        for event in events:
            self.event_dealer(event)
        
        # Scan the status of all servers
        for s in self.servers:
            status = s.get_status()
            if status['state'] == 'Delivery':
                self.vehicles[status['task'].vehicle_id].receive_delivery(status['task'])
                status['task'].deliver(self.time_slot)
                self.finished_task_num += 1
    
    # not done    
    def event_dealer(self, event):

        #TODO 2020/08/21
        # This event dealer should only take care of propagation. (at least so far)

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

    def deal_with_vehicles(self, new_tasks):
        for t in new_tasks:
            t.task_id = len(self.tasks)
            self.tasks.append(t)

            # TODO
            # Simulator should assign tasks to servers where vehicles are connected
            # Position info should come into place
            # Here, just assign to Server[self.time_slot%5]
            self.assign_task(self.time_slot%3, t)
        return


    # ---------------------------------
    # Here is for task-related method
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


    # -----------------------------
    # Code below is just about data collection
    def init_data(self):
        if self.data_wanted["all_slots_unfinished_task_num"]:
            self.data["all_slots_unfinished_task_num"] = []
        if self.data_wanted["all_slots_server_loading_task"]:
            self.data["all_slots_server_loading_task"] = []
        if self.data_wanted["all_slots_server_loading_new_task"]:
            self.data["all_slots_server_loading_new_task"] = []
        if self.data_wanted["all_slots_server_lodaing_propagation_task"]:
            self.data["all_slots_server_lodaing_propagation_task"] = []
        if self.data_wanted["all_slots_finished_task_num"]:
            self.data["all_slots_finished_task_num"] = []
        if self.data_wanted["all_slots_task_num"]:
            self.data["all_slots_task_num"] = []
        if self.data_wanted["tasks_info"]:
            self.data["tasks_info"] = []
        if self.data_wanted["delivered_tasks_info"]:
            self.data["delivered_tasks_info"] = []
        if self.data_wanted["events"]:
            self.data["events"] = []

    def record_data(self, recent_events):
        # add the info into history
        self.events.extend(recent_events)
        if self.data_wanted["all_slots_unfinished_task_num"]:
            self.data["all_slots_unfinished_task_num"].append(len(self.tasks) - self.finished_task_num)
        if self.data_wanted["all_slots_server_loading_task"]:
            self.data["all_slots_server_loading_task"].append([len(s.tasks) for s in self.servers])
        if self.data_wanted["all_slots_server_loading_new_task"]:
            self.data["all_slots_server_loading_new_task"].append([len(s.new_tasks) for s in self.servers])
        if self.data_wanted["all_slots_server_lodaing_propagation_task"]:
            self.data["all_slots_server_lodaing_propagation_task"].append([len(s.propagation_tasks) for s in self.servers])
        if self.data_wanted["all_slots_finished_task_num"]:
            self.data["all_slots_finished_task_num"].append(self.finished_task_num)
        if self.data_wanted["all_slots_task_num"]:
            self.data["all_slots_task_num"].append(len(self.tasks))
        return

    def get_pack_data(self):
        data = {
            'server_num': self.server_num,
            'tasks': [t.__dict__ for t in self.tasks],
            'events': [[e.__dict__ for e in event] for event in self.events]
        }
        return data

    def get_data(self):
        if self.data_wanted['tasks_info']:
            self.data['tasks_info'] = [t.__dict__ for t in self.tasks]
        if self.data_wanted['delivered_tasks_info']:
            for t in self.tasks:
                if t.is_delivered():
                    self.data['delivered_tasks_info'].append({
                        'id': t.task_id,
                        'name': t.name,
                        'waiting_time': t.get_waiting_time(),
                        'priority': t.priority,
                        'duration': t.duration
                    })

        if self.data_wanted['events']:
            for e in self.events:
                self.data['events'].append({
                    'server_id': e.server_id,
                    'name': e.name
                })
        return self.data


    # -----------------------------------
    # Some legacy code. 
    # Use for debugging.
    def print_info(self):
        # This can show each round task queue.
        # Provide quite good view of what's going on.
        print('finished task:', self.finished_task_num, 'all tasks:', len(self.tasks))
        print([len(s.tasks) for s in self.servers])
        print([len(s.propagation_tasks) for s in self.servers])
        print([len(s.new_tasks) for s in self.servers])
        return 

    