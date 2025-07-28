from io import TextIOWrapper
from intcode import Intcode

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.readline())
    comp.read_in(1)
    comp.run()
    print(comp.read_out()[-1])

    comp.reset()
    comp.read_in(5)
    comp.run()
    print(comp.read_out()[-1])
