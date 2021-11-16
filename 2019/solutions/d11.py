from io import TextIOWrapper
from intcode import Intcode, ReturnCode
from collections import defaultdict

class Direction:
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Robot:
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.dir = Direction.UP
    
    def turn_left(self):
        match self.dir:
            case Direction.UP:
                self.dir = Direction.LEFT
            case Direction.LEFT:
                self.dir = Direction.DOWN
            case Direction.DOWN:
                self.dir = Direction.RIGHT
            case Direction.RIGHT:
                self.dir = Direction.UP

    def turn_right(self):
        match self.dir:
            case Direction.UP:
                self.dir = Direction.RIGHT
            case Direction.LEFT:
                self.dir = Direction.UP
            case Direction.DOWN:
                self.dir = Direction.LEFT
            case Direction.RIGHT:
                self.dir = Direction.DOWN
    
    def step(self):
        self.xpos += self.dir[0]
        self.ypos += self.dir[1]
    
    def pos(self):
        return (self.xpos, self.ypos)

def paint_panels(brain, start_color):
    panels = defaultdict(int)
    robot = Robot()

    panels[robot.pos()] = start_color

    while True:
        brain.read_in(panels[robot.pos()])
        ret_code = brain.run()
        output = brain.read_out()

        if ret_code != ReturnCode.HALT:
            panels[robot.pos()] = output[0]
            if output[1] == 0:
                robot.turn_left()
            else:
                robot.turn_right()
            robot.step()
        else:
            break
    return panels

def main(in_file: TextIOWrapper):
    BLACK = 0
    WHITE = 1

    brain = Intcode(in_file.readline())

    print(len(paint_panels(brain, 0)))

    brain.reset()
    letter_panels = paint_panels(brain, 1)
    top_left = (0, 0)
    bot_right = (0, 0)
    for x, y in letter_panels:
        if x < top_left[0]:
            top_left = (x, top_left[1])
        elif x > bot_right[0]:
            bot_right = (x, bot_right[1])
        if y < top_left[1]:
            top_left = (top_left[0], y)
        elif y > bot_right[1]:
            bot_right = (bot_right[0], y)

    chars = [' ', u'\u2588']
    for y in range(bot_right[1], top_left[1] - 1, -1):
        for x in range(top_left[0], bot_right[0] + 1):
            print(chars[letter_panels[(x, y)]], end='')
        print()