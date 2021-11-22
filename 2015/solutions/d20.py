from io import TextIOWrapper

def factor_sum(house):
    s = 0
    i = 1
    limit = int((house+1)**0.5)
    while i <= limit:
        if house % i == 0:
            s += i
            div = house // i
            if div != i:
                s += div
        i += 1
    return s

def factor_sum_limit(house):
    s = 0
    i = 1
    c = 0
    limit = int((house+1)**0.5)
    while i <= limit and c < 50:
        if house % i == 0:
            s += i
            c += 1
            if house // i != i:
                s += house // i
                c += 1
        i += 1
    return s

def main(in_file: TextIOWrapper):
    goal = int(in_file.readline().strip())
    house = 0
    count = 0
    while count < goal:
        house += 360
        count = 10 * factor_sum(house)
    print(house)

    house = 0
    count = 0
    while count < goal:
        house += 360
        count = 11 * factor_sum_limit(house)
    print(house)
