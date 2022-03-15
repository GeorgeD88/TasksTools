import json


def write_json(data: dict, filename: str, indent=4):
    """ Writes data to JSON. """
    with open(filename + '.json', 'w+') as out_file:
        json.dump(data, out_file, indent=indent)

def read_json(filename: str):
    """ Reads data from JSON. """
    with open(filename + '.json', 'r') as in_file:
        data = json.load(in_file)
    return data
