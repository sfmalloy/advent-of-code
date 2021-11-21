from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    lines = [l.rstrip() for l in in_file.readlines()]

    total_diff = 0
    total_mem = 0
    for l in lines:
        idx = 1
        mem = len(l)
        str_mem = 0
        while idx < len(l) - 1:
            c = l[idx]
            str_mem += 1
            if c == '\\':
                idx += 1
                esc = l[idx]
                if esc == '\"' or esc == '\\':
                    idx += 1
                else:
                    idx += 3
            else:
                idx += 1
        total_diff += mem - str_mem
        total_mem += mem

    print(total_diff)

    total_new_mem = 0
    for l in lines:
        new_mem = 6
        for c in l[1:-1]:
            new_mem += 1
            if c == '\\' or c == '\"':
                new_mem += 1
        total_new_mem += new_mem

    print(total_new_mem - total_mem)
