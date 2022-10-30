from collections import defaultdict
from queue import PriorityQueue
from io import TextIOWrapper

def replace(orig, rep, mole, occurance):
    i = 0
    o = 0
    while o < occurance and i <= len(mole) - len(orig):
        if mole[i:i+len(orig)] == orig:
            o += 1
        i += 1
    i -= 1
    if o < occurance:
        return mole
    return mole[:i] + rep + mole[i+len(orig):]

def main(in_file: TextIOWrapper):
    reps = defaultdict(list)
    lines = in_file.readlines()
    for i in range(len(lines)-2):
        orig, rep = lines[i].strip().split(' => ')
        reps[orig].append(rep)
    
    mole = lines[-1].strip()
    unique = set()
    for orig, rep_list in reps.items():
        for rep in rep_list:
            i = 1
            curr = replace(orig, rep, mole, i)
            while curr != mole:
                unique.add(curr)
                i += 1
                curr = replace(orig, rep, mole, i)
    print(len(unique))

    unique = set()
    q = PriorityQueue()
    start = mole
    count = 0
    while start != 'e':
        for orig, rep_list in reps.items():
            for rep in rep_list:
                i = 1
                curr = replace(rep, orig, start, i)
                while curr != start:
                    unique.add(curr)
                    i += 1
                    curr = replace(rep, orig, start, i)
        for u in unique:
            q.put((len(u), u))
        _, start = q.get()
        unique = set()
        count += 1
    print(count)
