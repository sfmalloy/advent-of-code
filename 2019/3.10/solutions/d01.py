from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    modules = list(map(int, in_file.readlines()))
    t1 = t2 = 0
    for m in modules:
        curr = (m//3 - 2)
        t1 += curr
        leftover = 0
        while curr > 0:
            leftover += curr
            m = curr
            curr = (m//3 - 2)
        t2 += leftover
    print(f'Part 1: {t1}')
    print(f'Part 2: {t2}')
