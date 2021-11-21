from io import TextIOWrapper

def count_digit(num, i):
    digit = num[i]
    count = 0
    while i < len(num) and num[i] == digit:
        count += 1
        i += 1
    return count

def look_and_say(num):
    i = 0
    new = ''
    while i < len(num):
        count = count_digit(num, i)
        new += f'{count}{num[i]}'
        i += count
    return new

def main(in_file: TextIOWrapper):
    orig_s = in_file.readline().rstrip()
    s1 = orig_s
    s2 = orig_s
    for i in range(50):
        if i < 40:
            s1 = look_and_say(s1)
        s2 = look_and_say(s2)

    print(len(s1))
    print(len(s2))