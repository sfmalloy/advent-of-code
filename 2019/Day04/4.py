f = open("4.in", 'r')

begin, end = map(int, f.readline().strip().split('-'))

def check_double(n):
    last = n % 10
    n = n // 10
    while (n > 0):
        if (n % 10 == last):
            return True
        last = n % 10
        n = n //10
    return False

def check_increase(n):
    last = n % 10
    n = n // 10
    while (n > 0):
        if (n % 10 > last):
            return False
        last = n % 10
        n = n //10
    return True

def check_new_double(n):
    str_n = str(n)
    for c in str_n:
        if (str_n.count(c) == 2):
            return True

    return False

count1 = 0
count2 = 0
for i in range(begin, end):
    if (check_increase(i) and check_double(i)):
        count1 += 1
        if (check_new_double(i)):
            count2 += 1

print("Part 1: %d" % count1)
print("Part 2: %d" % count2)
