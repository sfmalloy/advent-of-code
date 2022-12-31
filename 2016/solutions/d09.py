from io import TextIOWrapper


def expand(string: str):
    print(string)
    i = 0
    size = 0
    while i < len(string):
        if string[i] != '(':
            i += 1
            size += 1
        else:
            end = string.index(')', i)
            num, reps = map(int, string[i+1:end].split('x'))
            i = end+1
            size += expand(string[i:i+num]) * reps
            i += num
    return size


def main(file: TextIOWrapper):
    string = file.read().strip()
    size = 0
    i = 0
    while i < len(string):
        if string[i] != '(':
            i += 1
            size += 1
        else:
            end = string.index(')', i)
            num, reps = map(int, string[i+1:end].split('x'))
            i = end+1
            size += num * reps
            i += num


    return size,expand(string)
