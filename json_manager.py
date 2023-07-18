import os
import json

def read_json():
    # Does the database exist? If not, create it
    if not os.path.isfile('data.json'):
        with open('data.json', 'w') as f:
            # Inserting an empty array
            json.dump([], f)
    
    # If the file was found
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

def write_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
