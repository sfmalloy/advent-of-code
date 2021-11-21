from io import TextIOWrapper
from math import sqrt

def factor_sum(house, limit):
    if house == 1:
        return 1
    s = 0
    i = 1
    while i <= limit:
        if house % i == 0:
            s += i
            if house // i != i:
                s += house // i
        i += 1
    return s

def main(in_file: TextIOWrapper):
    goal = int(in_file.readline().strip())
    # goal = 200
    house = 1
    count = 10
    while count < goal:
        house += 1
        count = 10 * factor_sum(house, int((house+1)**0.5))
        # print(house,count)
    print(house)

    # house = 1
    # count = 11
    # while count < goal:
    #     house += 1
    #     count = 11 * factor_sum(house, 50)
    #     print(count)
    # print(house)