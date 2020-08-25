from Task import Task
from random import randint, choice, uniform

class Vehicle():
    time_slot = 0
    config = {}
    def __init__(self, vehicle_id=0, position=None, direction=None):
        self.position = position
        self.direction = direction
        self.tasks = []
        self.vehicle_id = vehicle_id
        return

    def __str__(self):
        s = ''
        s = '\n*************************\n'
        s += 'Vehicle: {}\n'.format(str(self.vehicle_id))
        s += 'Task num ' + str(len(self.tasks))
        for task in self.tasks:
            s += '\n' + str(task)
        return s


    def run(self):
        # move position
        # generate task
        t = self.vehicle_random_generate_task()
        return t

    

    def receive_delivery(self, task):
        self.tasks.remove(task)
        return

    def vehicle_random_generate_task(self):
        # Testing: use the first config task
        task_config = self.config["tasks_config"][0]
        if uniform(0, 1) < task_config["occur_probability"]:
            t = self.vehicle_create_task(name=task_config["name"],
                    duration=randint(task_config["duration_range"][0], task_config["duration_range"][1]),
                    priority=task_config["priority"], request_time=self.time_slot, vehicle_id=self.vehicle_id) 
            return t
        return None

    def vehicle_create_task(self, name="", duration=1, have_done=0, 
                priority=0, request_time=0, detail="No task description", task_id=0, vehicle_id=0):
        # use this method to create task
        # so that we can make sure the created tasks are always added to the list.
        t = Task(name=name, duration=duration, have_done=have_done, 
                priority=priority, request_time=request_time,
                detail=detail, task_id=task_id, vehicle_id=vehicle_id)
        self.tasks.append(t)
        return t