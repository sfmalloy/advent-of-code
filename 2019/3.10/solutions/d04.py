from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    begin, end = map(int, in_file.readline().split('-'))

    count1 = count2 = 0
    for pwd in range(begin, end):
        digits = []
        while pwd > 0:
            digits.append(pwd % 10)
            pwd //= 10
        unique = set(digits)

        if len(unique) < len(digits):
            increasing = True
            for i in range(1, len(digits)):
                if digits[i-1] > digits[i]:
                    increasing = False
                    break
            if increasing:
                count1 += 1
                for d in unique:
                    if digits.count(d) == 2:
                        count2 += 1
                        break

    print(count1)
    print(count2)
