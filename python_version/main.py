from Simulation import Simulator
from Task import Task
from util import read_config

def read_input_task(filename):
    res = []
    with open(filename, 'r') as f:
        while True:
            s = f.readline().split()
            if not s:
                break
            res.append((int(s[0]), Task(s[1], int(s[2]), int(s[3]))))
    return res

# Build a Simulator 
config = read_config('config.json')
s = Simulator(config)

# Add some initial tasks to simulator
tasks = read_input_task('input_task.dat')
s.add_tasks_to_servers(tasks) 
# s.run()

while True:
    command = input('input command...\n')
    if command == 's':
        s.show_status()
    if command == 'r':
        s.run_one()
        print('run')
    
