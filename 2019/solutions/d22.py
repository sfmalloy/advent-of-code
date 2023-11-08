from io import TextIOWrapper
from typing import Self, Optional
from dataclasses import dataclass

# Classes
@dataclass
class Card:
    val: int
    deck_size: int
    next: Optional[Self] = None

    def print(self):
        seen = set()
        curr = self
        seen.add(curr.val)
        while True:
            print(curr.val, end=' ')
            curr = curr.next
            if curr == self:
                break
            seen.add(curr.val)
        print()
    

def main(file: TextIOWrapper):
    commands = file.readlines()
    part1(commands)


def part1(commands: list[str]):
    top, bottom = new_deck(10007)

    for cmd in commands:
        words = cmd.split()
        match words:
            case ['cut', i]:
                top, bottom = cut(top, bottom, int(i))
            case ['deal', 'into', 'new', 'stack']:
                top, bottom = reverse(top, bottom)
            case ['deal', 'with', 'increment', i]:
                top, bottom = deal(top, int(i))

    curr = top
    pos = 0
    while curr.val != 2019:
        curr = curr.next
        pos += 1
    print(pos)



# Helper Functions
def new_deck(deck_size: int):
    top = Card(0, deck_size)
    bottom = top
    for val in range(1, deck_size):
        tmp = Card(val, deck_size)
        bottom.next = tmp
        bottom = bottom.next
    bottom.next = top
    return top, bottom


def cut(top: Card, bottom: Card, idx: int) -> Card:
    if idx < 0:
        idx += top.deck_size
    cut_point = top
    for _ in range(idx-1):
        cut_point = cut_point.next

    n = cut_point.next
    cut_point.next = n
    bottom.next = top
    return n, cut_point


def reverse(top: Card, bottom: Card):
    prev = bottom
    curr = top
    for _ in range(top.deck_size):
        tmp = curr.next
        curr.next = prev
        prev = curr
        curr = tmp
    return bottom, top


def deal(top: Card, inc: int):
    t, b = new_deck(top.deck_size)
    old = top
    new = t
    for _ in range(top.deck_size):
        new.val = old.val
        old = old.next
        for _ in range(inc):
            new = new.next
    return t, b


def get(top: Card, idx: int):
    curr = top
    for _ in range(idx):
        curr = curr.next
    return curr


'''
119315717514047 cards
101741582076661 shuffles

def new_pos(pos, x, N):
    if pos % x == 0:
        return pos // x
    return ((pos % x) * (pos // x)) + ((N // x) + (x - (N % x))) * (pos % x)

'''
