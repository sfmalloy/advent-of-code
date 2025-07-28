from io import TextIOWrapper
from intcode import Intcode

def search_row(comp, start_x, y, x_limit):
    beamed = 0
    new_x = 0
    x = start_x
    while x < x_limit:
        comp.read_in(x, y)
        comp.run()
        is_beam = comp.read_out()[0]
        beamed += is_beam
        comp.reset()
        if new_x == 0 and is_beam:
            new_x = x+1
        elif new_x != 0 and not is_beam:
            break
        x += 1
    return beamed, new_x

def check_is_beam(comp, x, y):
    comp.read_in(x, y)
    comp.run()
    is_beam = comp.read_out()[0]
    comp.reset()
    return is_beam

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.readline())

    beamed = 0
    start_x = 0
    for y in range(50):
        res, start_x = search_row(comp, start_x, y, 50)
        beamed += res

    X = 0
    Y = 4
    edges = []
    while not check_is_beam(comp, X, Y):
        X += 1
    while not check_is_beam(comp, X+99, Y-99):
        Y += 1
        while not check_is_beam(comp, X, Y):
            X += 1
        edges.append((X,Y))

    print(beamed)
    print(X*10000+Y-99)
