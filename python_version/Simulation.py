import os
import sys
sys.path.append(".")
from Task import Task
from Event import Event
from Server import Server

class Simulator:
    def __init__(self, server_num, all_tasks):
        self.server_num = server_num # number of servers, ex: 7
        # To differentiate with tasks in server, name it "all_tasks"
        self.all_tasks = all_tasks # can be a list of tuple [(server_id, Task)]
        Server.server_sum = server_num
        Server.all_tasks = [[] for i in range(server_num)]
        self.servers = [Server(i) for i in range(server_num)] # list of Server
        self.initialize_servers()
        self.events = [] # events of each server in time slot
        self.time_slot = 1

    def __str__(self):
        s = ''
        s += 'Number of servers: {}\n'.format(len(self.servers))
        for i in range(len(self.servers)):
            s += 'Server {}: {}\n'.format(i, str(self.servers[i]))
        return s

    def initialize_servers(self):
        for task in self.all_tasks:
            self.servers[task[0]].add_task(task[1])
        return

    def show_status(self):
        # print out current status
        # including: 
        # All Server status
        # What round is this?
        print("======= Time Slot " + str(self.time_slot) + " =======")
        return

    def run(self):
        # Run the simulation. Can be a while loop?
        # run all server 
        # and then run synchronization
        while True:
            if self.time_slot > 15:
                break
            recent_events = []
            self.show_status()
            for i in range(self.server_num):
                e = self.run_server(i)
                print('Server ' + str(i) + ': ' + str(e))
                recent_events.append(e)

                
                
            
            self.run_sync(recent_events)

            self.record(recent_events)
            self.time_slot += 1
   
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
        pass

    
    def event_dealer(self, event):
        if event.name == "delivery":
            event.info["source"]
        pass


    def assign_task(self, server_id, task):
        self.servers[server_id].tasks.add_task(task)
        self.servers[server_id].new_task = True
        return







