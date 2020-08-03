class Simulator:
    def __init__(self, server_num, all_tasks):
        self.server_num = server_num # number of servers, like 7
        # To differentiate with tasks in server, name it "all_tasks"
        self.all_tasks = all_tasks # can be a list of tuple [(server_id, Task)]
        self.servers = [Server(i) for i in range(server_num)] # list of Server
        self.initialize_servers()
        self.events = [] # list of Event
        self.time_slot = 1
    
    def initialize_servers(self):
        # add tasks into servers
        pass

    def show_status(self):
        # print out current status
        # including: 
        # All Server status
        # What round is this?
        print("======= Time Slot " + str(self.time_slot) + " =======")
        pass

    def run(self):
        # Run the simulation. Can be a while loop?
        # run all server 
        # and then run synchronization
        while True:
            if self.time_slot > 10:
                break
            recent_events = []
            self.show_status()
            for i in range(self.server_num):
                recent_events.append(self.run_server(i))
            
            self.run_sync(recent_events)

            self.record(recent_events)
            self.time_slot += 1
   
    def run_server(self, server_id):
        # Time to run this server~
        # get event from server
        event = self.servers[server_id].run()
        return event
    
    def run_sync(self, events):
        # already get all events from servers in this round
        # pass them to corresponding server
        for event in events:
            self.event_dealer(event)
    
    def record(self, recent_events):
        self.events.extend(recent_events)
        pass

    
    def event_dealer(self, event):
        pass




class Server:
    def __init__(self, tasks):
        self.tasks = tasks # a list of Task

    def event_handler(self, event):
        # Handle the event. Maybe add tasks to taskQueue? Or anything...
        pass
    
    def run(self):
        # return event. can be none?
        pass


class Task:
    def __init__(self, name):
        self.name = name
        return

class Event:
    def __init__(self):
        return

        
s = Simulator(5, [])
s.run()
