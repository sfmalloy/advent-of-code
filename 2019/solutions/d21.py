from io import TextIOWrapper
from intcode import Intcode


def survey(comp: Intcode, asm: str):
    comp.read_in_ascii(*map(str, asm))
    comp.run()
    output = comp.read_out_ascii()
    comp.reset()
    return output


def main(file: TextIOWrapper):
    # did this entire day by hand for fun

    comp = Intcode(file.readline())

    # instructions = {'AND','OR','NOT'}
    # X = {'A','B','C','D','T','J'}
    # Y = {'T','J'}
    # jump distance is 4 tiles
    walk = '\n'.join('''
        NOT C T
        AND D T
        OR T J
        NOT A T
        OR T J
        WALK
    '''.lstrip().split('\n        '))
    
    #             1   2   3   4   5   6   7   8   9
    # X = {'A','B','C','D','E','F','G','H','I','T','J'}
    # everything else is the same
    run = '\n'.join('''
        NOT B T
        AND D T
        OR T J
        NOT C T
        AND D T
        AND H T
        OR T J
        NOT A T
        AND D T
        OR T J
        RUN
    '''.lstrip().split('\n        '))

    print(survey(comp, walk).split('\n')[-1])
    print(survey(comp, run).split('\n')[-1])
