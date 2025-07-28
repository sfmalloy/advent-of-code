from io import TextIOWrapper
from .assembunny import Assembunny

def main(file: TextIOWrapper):
    lines = file.readlines()
    comp1 = Assembunny(lines, [0, 0, 0, 0])
    comp2 = Assembunny(lines, [0, 0, 1, 0])
    comp1.run()
    comp2.run()
    return comp1.mem[0], comp2.mem[0]
