from io import TextIOWrapper
from intcode import Intcode
from itertools import permutations
from copy import deepcopy

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.read())
    signal = 0
    for phases in permutations(range(5)):
        output = 0
        for phase in phases:
            comp.read_in(phase, output)
            comp.run()
            output = comp.read_out()[0]
            comp.reset()
        signal = max(signal, output)
    print(signal)

    signal = 0
    for phases in permutations(range(5, 10)):
        output = 0
        idx = 0
        comps = [deepcopy(comp) for _ in range(len(phases))]
        for c,p in zip(comps, phases):
            c.read_in(p)
        while not comps[-1].is_finished():
            comps[idx].read_in(output)
            comps[idx].run()
            output = comps[idx].read_out()[-1]
            idx = (idx + 1) % len(phases)
        signal = max(signal, output)
            
    print(signal)
