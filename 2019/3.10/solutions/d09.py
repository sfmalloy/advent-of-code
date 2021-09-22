from io import TextIOWrapper
from intcode import Memory

def main(in_file: TextIOWrapper):
    mem = Memory()
    mem[10] = 5
    print(len(mem))
    print(mem)
