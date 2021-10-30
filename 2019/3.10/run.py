import os
import importlib
from optparse import OptionParser
from timeit import default_timer as curr_time

def day_num_file(day_num):
    if int(day_num) < 10:
        return f'0{day_num}'
    return day_num

def run_all():
    day_num = 1
    total_time = 0
    curr_time = 0
    while day_num <= 25:
        print(f'Day {day_num}:')
        curr_time = run_single(day_num)
        if curr_time > 0:
            total_time += curr_time
            day_num += 1
        else:
            break
        print()
    return total_time

def run_single(day_num, input_file=None):
    day_num = day_num_file(day_num)
    time = 0

    if input_file is None:
        input_file = os.path.join('inputs', f'd{day_num}.in')
    solution_file = os.path.join('solutions', f'd{day_num}.py')

    if not os.path.exists(solution_file):
        print(f'Day {day_num} solution file not found')
        return -1
    elif not os.path.exists(input_file):
        print(f'Input file {input_file} not found')
        return -1

    with open(input_file) as f:
        solution = importlib.import_module(f'.d{day_num}', package='solutions')
        start = curr_time()
        solution.main(f)
        end = curr_time()
        time = 1000 * (end - start)

    return time

def main():
    parser = OptionParser()
    parser.add_option('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '\
        'default uses input file from inputs directory.')
    parser.add_option('-a', '--all', action='store_true', dest='run_all', 
        default=False, help='Run all days')
    parser.add_option('-f', '--file', dest='file', help='Specify different input file from default')

    options, _ = parser.parse_args()

    if options.run_all:
        time = run_all()
        print(f'\nTime: {time:.3f}ms')
    elif options.day is not None:
        time = run_single(options.day, options.file)
        if time > 0:
            print(f'Time: {time:.3f}ms')

if __name__ == '__main__':
    main()
