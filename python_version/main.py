from Simulation import Simulator
from Task import Task
from util import read_config
import json
import matplotlib.pyplot as plt

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

# with open('evaluation_data.json', 'w') as f:
#     json.dump(data, f)


# plt.plot(data['data_of_slot'])
# plt.show()
s.run(50)
print(s.get_data())

    
# print(data['data_of_slot']['server_loading_task'])
# print(data['data_of_slot']['server_loading_new_task'])
# print(data['data_of_slot']['unfinished_task_num'])



# This is for testing
# while True:
#     command = input('input command...\n')
#     if command == 's':
#         s.show_status()
#     if command == 'r':
#         s.run_one()
#         print('run')
#     if command == 'd':
#         data = json.dumps(s.get_pack_data())
        
#         print(data)
    
