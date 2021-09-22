from intcode import Intcode

with open('euler1.intcode') as f:
    prog = ''
    for l in f.readlines():
        prog += l.strip()
    comp = Intcode(prog)
    comp.run()
    print(comp.read_out())
