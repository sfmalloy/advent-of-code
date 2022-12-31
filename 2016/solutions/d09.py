from io import TextIOWrapper
from dataclasses import dataclass


def main(file: TextIOWrapper):
    string = file.read().strip()
    i = 0
    decomp = ''
    while i < len(string):
        if string[i] != '(':
            decomp += string[i]
            i += 1
        else:
            end = string.index(')', i)


    return -1,-1
