from io import TextIOWrapper
from intcode import Intcode

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.readline())
    comp.read_in(1)
    comp.run()

    print(comp.read_out()[0])

    comp.reset()
    comp.read_in(2)
    comp.run()

    print(comp.read_out()[0])
