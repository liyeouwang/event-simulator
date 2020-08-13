from random import randint, choice
from util import read_config



data = read_config('config.json')

SERVER_NUM = data['server_num']
TASKS = [t['name'] for t in data['tasks_config']]
DATA_NUM = 10
FILENAME = "input_task.dat"

with open(FILENAME, "w") as f:
    for i in range(DATA_NUM):
        s = str(randint(0, SERVER_NUM-1)) + ' ' + choice(TASKS) +' '+ str(randint(1, 10)) +' '+ str(0)+'\n'
        f.write(s)
f.close()