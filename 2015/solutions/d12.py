from io import TextIOWrapper
import json

def list_sum(l, ignore_red):
    s = 0
    for elem in l:
        if isinstance(elem, dict):
            s += dict_sum(elem, ignore_red)
        elif isinstance(elem, list):
            s += list_sum(elem, ignore_red)
        elif isinstance(elem, int):
            s += int(elem)
    return s

def dict_sum(d, ignore_red):
    s = 0
    for key in d:
        if isinstance(d[key], dict):
            s += dict_sum(d[key], ignore_red)
        elif isinstance(d[key], list):
            s += list_sum(d[key], ignore_red)
        elif ignore_red and d[key] == 'red':
            return 0
        elif isinstance(d[key], int):
            s += int(d[key])
    return s

def main(in_file: TextIOWrapper):
    j = json.load(in_file)
    print(dict_sum(j, False))
    print(dict_sum(j, True))