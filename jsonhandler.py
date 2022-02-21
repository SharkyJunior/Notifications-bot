import json

def LoadJson(path):
    data = json.load(open(path))
    return data

def DumpJson(path, data):
    data = json.dumps(data)
    f = open(path, mode="w")
    f.write(data)