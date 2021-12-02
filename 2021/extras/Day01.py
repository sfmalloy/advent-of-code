def main():
    with open('../inputs/Day01.in') as infile:
        inp = [int(line.strip()) for line in infile.readlines()]
        # inp = [199,200,208,210,200,207,240,269,260,263]

        i = 0
        inc = 0
        inc3 = 0
        prevs = 0
        while i < len(inp) - 1:
            if inp[i] < inp[i+1]:
                inc += 1
            if i < len(inp) - 2:
                s = sum(inp[i:i+3])
                print(s)
                if prevs != 0 and s > prevs:
                    inc3 += 1
                prevs = s
            i += 1
        print(inc)
        print(inc3)

if __name__ == '__main__':
    main()