import json

def LoadJson(path):
    data = json.load(open(path))
    return data

def DumpJson(path, data):
    data = json.dump(data)
    f = open(path)
    f.write(data)