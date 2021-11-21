from io import TextIOWrapper

def inc(s):
    z = len(s) - 1
    while z >= 0 and s[z] == 'z':
        z -= 1
    if z == -1:
        return 'a' * (len(s)+1)
    return s[:z] + chr(ord(s[z])+1) + ('a' * (len(s)-z-1))

def check_str(s):
    pairs = set()
    inc = False
    for i in range(len(s)):
        if s[i] in {'i', 'l', 'o'}:
            return False
        if i < len(s)-1 and s[i] == s[i+1]:
            pairs.add(s[i:i+2])
        inc = inc or i < len(s)-2 and ord(s[i])+1 == ord(s[i+1]) and ord(s[i+1])+1 == ord(s[i+2])
    return len(pairs) >= 2 and inc

def main(in_file: TextIOWrapper):
    pwd = in_file.readline().rstrip()

    while not check_str(pwd):
        pwd = inc(pwd)
    print(pwd)

    pwd = inc(pwd)
    while not check_str(pwd):
        pwd = inc(pwd)
    print(pwd)