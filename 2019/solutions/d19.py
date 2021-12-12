from io import TextIOWrapper
from intcode import Intcode

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.readline())

    beamed = 0
    start_x = 0
    for y in range(50):
        new_start_x = 0
        x = start_x
        while x < 50:
            comp.read_in(x, y)
            comp.run()
            is_beam = comp.read_out(fast=True)[-1]
            comp.reset(flush=False)
            beamed += is_beam
            if new_start_x == 0 and is_beam:
                new_start_x = x+1
            elif new_start_x != 0 and not is_beam:
                break
            x += 1
        start_x = new_start_x
    print(beamed)
