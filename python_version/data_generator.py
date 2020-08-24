from random import randint, choice
from util import read_config



data = read_config('config.json')

SERVER_NUM = data['server_num']
TASKS = [t['name'] for t in data['tasks_config']]
TASKS_CONFIG = data['tasks_config']
DATA_NUM = 10
FILENAME = "input_task.dat"

with open(FILENAME, "w") as f:
    for i in range(DATA_NUM):
        task = choice(TASKS_CONFIG)
        s = str(randint(0, SERVER_NUM-1)) + ' ' + task["name"] +' '+ str(randint(task["duration_range"][0], task["duration_range"][1])) +' '+ str(task["priority"])+'\n'
        f.write(s)
f.close()