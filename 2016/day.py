#!/bin/python

import os
import sys

def file_num(day_num):
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def main(day_num):
    os.system(f'cp solutions/template.py solutions/d{file_num(day_num)}.py')
    os.system(f'echo "from . import d{file_num(day_num)}" >> solutions/__init__.py')
    os.system(f'python download.py -d {day_num}')

if __name__ == '__main__':
    main(int(sys.argv[1]))
