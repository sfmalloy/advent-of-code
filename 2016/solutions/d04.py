import re
from io import TextIOWrapper
from collections import defaultdict
from functools import cmp_to_key


def compare(a: tuple[int, str], b: tuple[int, str]):
    if a[0] > b[0]:
        return -1
    elif a[0] == b[0] and a[1] < b[1]:
        return -1
    return int(a != b)


def main(file: TextIOWrapper):
    lines = file.readlines()
    s = 0
    p2 = -1
    for line in lines:
        counts = defaultdict(int)
        room = line.strip().split('-')
        room_id = int(re.search(r'\d+', room[-1]).group())
        checksum = re.search(r'[a-z]{5}', room[-1]).group()
        room.pop()
        name = ''.join(room)
        for char in name:
            counts[char] += 1
        sorted_counts = ''.join(map(lambda p: p[1], sorted([(v,k) for k,v in counts.items()], key=cmp_to_key(compare))))[:5]
        if sorted_counts == checksum:
            s += room_id
            if p2 == -1:
                shift_amt = room_id % 26
                spaced_name = ' '.join(room)
                shifted = ''
                for char in spaced_name:
                    if char != ' ':
                        shifted += chr(((ord(char)-ord('a')+shift_amt) % 26) + ord('a'))
                    else:
                        shifted += ' '
                if shifted == 'northpole object storage':
                    p2 = room_id
    return s,p2
