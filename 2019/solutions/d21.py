from io import TextIOWrapper
from intcode import Intcode


def survey(comp: Intcode, asm: str):
    comp.read_in_ascii(*map(str, asm))
    comp.run()
    output = comp.read_out_ascii()
    comp.reset()
    return output


def main(file: TextIOWrapper):
    comp = Intcode(file.readline())

    # instructions = {'AND','OR','NOT'}
    # inputs       = {'A','B','C','D','T','J'}
    # outputs      = {'T','J'}
    # jump distance is 4 tiles
    walk = '\n'.join('''
        NOT B T
        AND C T
        AND T J
        NOT C T
        AND D T
        OR T J
        NOT A T
        AND C T
        OR T J
        WALK
    '''.lstrip().split('\n        '))
    
    # outputs = {'A','B','C','D','E','F','G','H','I','T','J'}
    # everything else is the same
    run = '\n'.join('''
        RUN
    '''.lstrip().split('\n        '))

    print(survey(comp, walk).split('\n')[-1])
    print(survey(comp, run))
