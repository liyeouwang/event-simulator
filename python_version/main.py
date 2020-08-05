from Simulation import Simulator
from Task import Task

def read_input_task(filename):
    res = []
    with open(filename, 'r') as f:
        while True:
            s = f.readline().split()
            if not s:
                break
            res.append((int(s[0]), Task(s[1], int(s[2]), int(s[3]))))
    return res



tasks = read_input_task('input_task.dat')
# s = Simulator(5, [(0, Task("1", "hello world")), (0, Task("1", "hello world")), (1, Task("1", "hello world")), (1, Task("2", "hello world")), (3, Task("3", "hello world")), (1, Task("4", "hello world"))])
# print(tasks)
s = Simulator(5, tasks)
print(s)
s.run()