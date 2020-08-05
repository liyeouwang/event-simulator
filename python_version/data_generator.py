from random import randint, choice

SERVER_NUM = 5
DATA_NUM = 15
TASKS = ["video_streaming", "trolley_problem", "dense_computing"]
FILENAME = "input_task.dat"

with open(FILENAME, "w") as f:
    for i in range(DATA_NUM):
        s = str(randint(0, SERVER_NUM-1)) + ' ' + choice(TASKS) +' '+ str(randint(1, 10)) +' '+ str(0)+'\n'
        f.write(s)
f.close()