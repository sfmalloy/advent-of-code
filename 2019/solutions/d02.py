from io import TextIOWrapper
from intcode import Intcode

def main(in_file: TextIOWrapper):
    comp = Intcode(in_file.read().strip())
    
    # Part 1
    comp.program[1] = 12
    comp.program[2] = 2
    comp.run()
    print(comp.program[0])

    # Part 2
    noun = verb = output = -1
    while noun < 100:
        while verb < 100:
            comp.reset()
            comp.program[1] = noun
            comp.program[2] = verb
            comp.run()
            output = comp.program[0]
            if output == 19690720:
                break
            verb += 1
        if output == 19690720:
            print(100 * noun + verb)
            break
        verb = 0
        noun += 1