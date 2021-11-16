from io import TextIOWrapper

from intcode import Intcode

class bot:
    def __init__(self, screen):
        self.N = 0
        self.E = 1
        self.S = 2
        self.W = 3

        self.chr_to_num = dict(zip('^>v<', [0,1,2,3]))
        self.num_to_chr = '^>v<'

        self.screen = [[c for c in l] for l in screen]

        self.x = 0
        self.y = 0

        found = False
        for i in range(self.rows()):
            for j in range(self.cols()):
                if self.screen[i][j] == '^':
                    self.x = j
                    self.y = i
                    found = True
                    break
            if found:
                break
        self.chr = screen[self.y][self.x]
        self.dir = self.chr_to_num[self.chr]
        self.facing = self.num_to_chr[self.dir]
    def rows(self):
        return len(self.screen)
    def cols(self):
        return len(self.screen[0])
    def turn(self, direction):
        if direction == 'R':
            self.update(self.num_to_chr[(self.dir+1) % 4])
        else:
            self.update(self.num_to_chr[(self.dir+3) % 4])
    def step(self, do_move=True):
        new_x = self.x
        new_y = self.y
        if self.dir == self.N:
            new_y -= 1
        elif self.dir == self.S:
            new_y += 1
        elif self.dir == self.E:
            new_x += 1
        elif self.dir == self.W:
            new_x -= 1
        if 0 <= new_x < self.cols() and 0 <= new_y < self.rows() and self.screen[new_y][new_x] != '.':
            if do_move:
                self.screen[self.y][self.x] = 'O'
                self.x = new_x
                self.y = new_y
                self.update(self.chr)
            return True
        return False
    def update(self, new_chr):
        self.screen[self.y][self.x] = new_chr
        self.chr = self.screen[self.y][self.x]
        self.dir = self.chr_to_num[self.chr]
    def find_open(self):
        self.turn('R')
        if self.step(False):
            self.turn('L')
            return 'R'
        self.turn('R')
        self.turn('R')
        if self.step(False):
            self.turn('R')
            return 'L'
        return None
    def __repr__(self):
        rep = ''
        for i in range(self.rows()):
            for j in range(self.cols()):
                rep += self.screen[i][j]
            rep += '\n'
        return rep

def find_pattern(s, start):
    end = 3
    while s.count(s[start:end]) > 2 and ('A' not in s[start:end] and 'B' not in s[start:end]):
        end = s.find(',', end+1)
    while s[end] in 'AB,LR':
        end -= 1
    return s[start:end+1]

def main(in_file: TextIOWrapper):
    raw_prog = in_file.readline()
    comp = Intcode(raw_prog)

    comp.run()
    screen_ascii = comp.read_out()
    screen = []
    line = ''
    for s in screen_ascii:
        if s != 10:
            line += chr(s)
        elif len(line) > 0:
            screen.append(line)
            line = ''

    x = y = 0
    p1 = 0
    for i in range(1, len(screen)-1):
        for j in range(1, len(screen[i])-1):
            if screen[i][j] == '#':
                if screen[i-1][j] == screen[i+1][j] == screen[i][j-1] == screen[i][j+1] == screen[i][j]:
                    p1 += i*j
    print(p1)

    b = bot(screen)
    cmd = []
    while b.find_open() is not None:
        turn_dir = b.find_open()
        cmd.append(turn_dir)
        b.turn(turn_dir)

        step_count = 0
        while b.step():
            step_count += 1
        cmd.append(step_count)

    cmd_str = ''
    for i in range(len(cmd)):
        cmd_str += str(cmd[i])
        if i < len(cmd)-1:
            cmd_str += ','

    start = 0
    patterns = {}
    letter = 'A'
    for i in range(3):
        patt = find_pattern(cmd_str, start)
        patterns[letter] = patt
        a = 0
        b = cmd_str.find(patt)
        while cmd_str.count(patt) > 0 and cmd_str.find(patt) != -1:
            cmd_str = cmd_str[a:b] + letter + cmd_str[b+len(patt):]
            b = cmd_str.find(patt)
        letter = chr(ord(letter)+1)
        if i < 2:
            while cmd_str[start] in 'ABC':
                start = cmd_str.find(',', start+1)+1

    comp = Intcode(raw_prog)
    comp.program[0] = 2
    ascii_code = []
    for c in cmd_str:
        ascii_code.append(ord(c))
    ascii_code.append(10)
    for func in patterns:
        for c in patterns[func]:
            ascii_code.append(ord(c))
        ascii_code.append(10)
    ascii_code.append(ord('n'))
    ascii_code.append(10)

    comp.read_in(*ascii_code)
    comp.run()
    output = comp.read_out()
    print(output[-1])
