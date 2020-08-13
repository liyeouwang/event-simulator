import json

def read_config(filename):
    f = open(filename)
    data = json.load(f)
    return data