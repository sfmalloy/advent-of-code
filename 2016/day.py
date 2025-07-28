#!/bin/python

import sys

def file_num(day_num):
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def main(day_num):
    with (
        open('solutions/template.py') as template,
        open(f'solutions/d{file_num(day_num)}.py', 'w') as day
    ):
        day.write(template.read())


if __name__ == '__main__':
    main(int(sys.argv[1]))
