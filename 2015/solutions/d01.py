from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    lisp = in_file.readline().strip()
    paren = {'(': 1, ')': -1}
    s = 0
    basement = 0
    for i, p in enumerate(lisp):
        s += paren[p]
        if s < 0 and basement == 0:
            basement = i + 1
    print(s)
    print(basement)
