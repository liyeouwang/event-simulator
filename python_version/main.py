from Simulation import Simulator
from Task import Task
from util import read_config
import json
import matplotlib.pyplot as plt
import os

def read_input_task(filename):
    res = []
    with open(filename, 'r') as f:
        while True:
            s = f.readline().split()
            if not s:
                break
            res.append((int(s[0]), Task(s[1], int(s[2]), priority=int(s[3]))))
    return res

def type_to_control(config):
    # This is for testing
    s = Simulator(config)

    while True:
        command = input('input command...\n')
        if command == 's':
            s.show_status()
        if command == 'sv':
            s.show_vehicle_status()
        if command == 'ss':
            s.show_server_status()
        if command == 'r':
            s.run_one()
            print('run')
        if command == 'd':
            data = json.dumps(s.get_pack_data())
        
            print(data)

def bad_experiment():
    # This experiment use bad evaluating metrics

    # Set the independent variables
    max_experiment = [2, 5, 10, 25, 50, 100]

    # Set the experiment environment
    experiment_dir = './e1/'
    config = read_config('config.json')
    os.mkdir(experiment_dir)
    with open(experiment_dir + 'config.json', 'w') as outfile:
        json.dump(config, outfile)

    for m in max_experiment:
        config["server_max_task"] = m
        a = [1, 2, 3, 4]
        fig, ((a[0], a[1]), (a[2], a[3])) = plt.subplots(2, 2)
        for n in range(4):
            s = Simulator(config)
            s.run(300)
            fig.suptitle('max=, 0.25')
            avg_awaiting_time = []
            total = 0
            for i, t in enumerate(s.get_data()["delivered_tasks_info"]):
                total += t['waiting_time']
                avg_awaiting_time.append(total/(i+1))
            a[n].plot(avg_awaiting_time)
        fig.savefig(experiment_dir + str(m)+'.png''')
        plt.close(fig)

def experiment():
    # Set the independent variables
    # max_experiment = [2, 5, 10, 25, 50, 100]

    # Set the experiment environment
    # experiment_dir = './e2/'
    config = read_config('config.json')
    # os.mkdir(experiment_dir)
    # with open(experiment_dir + 'config.json', 'w') as outfile:
    #     json.dump(config, outfile)

    s = Simulator(config)
    s.run(3000)
    config['data_collection_interval'] = 10
    data = s.get_data()
    plt.plot(data["all_slots_task_num"])
    plt.plot(data["all_slots_finished_task_num"])

    plt.show()

    # s = Simulator(config)
    # fig, ((a[0], a[1]), (a[2], a[3])) = plt.subplots(2, 2)
    
    # fig.suptitle('max=5, 0.25')
    # for n in range(4):
    #     s = Simulator(config)
    #     s.run(30000)
    #     task_waiting_time = []
    #     avg_awaiting_time = []
    #     total = 0
    #     for i, t in enumerate(s.get_data()["delivered_tasks_info"]):
    #         task_waiting_time.append(t['waiting_time'])
    #         total += t['waiting_time']
    #         avg_awaiting_time.append(total/(i+1))
    #     a[n].plot(avg_awaiting_time)
    #     # plt.plot(avg_awaiting_time)
    #     # plt.show()
    # plt.show()

def main():
    # experiment()
    config = read_config('config.json')
    type_to_control(config)
 
    return


if __name__ == "__main__":
    main()

        
