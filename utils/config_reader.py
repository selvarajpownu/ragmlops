import os
import json

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../config/config.json")

def configData():
    with open(filename) as f:
        data = json.load(f)
    
    return data

