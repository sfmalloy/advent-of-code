from io import TextIOWrapper
from collections import defaultdict

def nice_one(lines):
    vowels = 'aeiou'
    bad = {'ab','cd','pq','xy'}
    nice = 0
    for s in lines:
        vowel = 0
        for v in vowels:
            if v in s:
                vowel += s.count(v)
        if vowel >= 3:
            double = False
            for i in range(len(s)-1):
                if s[i] == s[i+1]:
                    double = True
                    break
            if double:
                invalid = False
                for b in bad:
                    if b in s:
                        invalid = True
                        break
                if not invalid:
                    nice += 1
    return nice

def nice_two(lines):
    nice = 0
    for l in lines:
        found_pair = False
        pairs = defaultdict(int)
        i = 0
        while i < len(l) - 1:
            p = f'{l[i]}{l[i+1]}'
            pairs[p] += 1
            if pairs[p] > 1:
                found_pair = True
                break
            if i < len(l) - 2 and l[i] == l[i+1] == l[i+2]:
                i += 1
            i += 1
        if found_pair:
            for i in range(len(l)-2):
                if l[i] == l[i+2]:
                    nice += 1
                    break
    return nice

def main(in_file: TextIOWrapper):
    lines = in_file.readlines()
    print(nice_one(lines))
    print(nice_two(lines))
