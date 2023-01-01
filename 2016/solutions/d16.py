from io import TextIOWrapper
from dataclasses import dataclass


def step(a: str):
    temp = a
    b = 0
    bit_len = 0
    while temp > 0:
        b <<= 1
        b |= temp & 1
        temp >>= 1
        bit_len += 1
    b = ~b + (1 << (max(bit_len, 1)))
    a <<= bit_len+1
    a |= b
    return a


def main(file: TextIOWrapper):
    print(bin(step(int('111100001010', 2))))
    return -1,-1
