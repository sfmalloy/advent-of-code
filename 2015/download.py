import os
import requests
from optparse import OptionParser

def print_file(filename):
    with open(filename) as f:
        print(f.read())

def create_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def day_num_file(day_num):
    if int(day_num) < 10:
        return f'0{day_num}'
    return day_num

def main():
    parser = OptionParser()
    parser.add_option('-d', '--day', dest='day', help='Downloads day <d> input if not already downloaded.')

    try:
        options, _ = parser.parse_args()
        day_num = options.day
        filename = os.path.join('inputs', f'd{day_num_file(day_num)}.in')
        year = 2015

        if os.path.exists(filename):
            print_file(filename)
        else:
            cookies = {'session': os.environ['AOC_SESSION']}
            request = requests.get(f'https://adventofcode.com/{year}/day/{day_num}/input', cookies=cookies)
            if request.status_code != 200:
                print(f'Error in retrieving input: Code {request.status_code} (Try resetting your session cookie)')
                exit(-1)
            create_file(filename, request.text)
            print_file(filename)
            print(f'File saved as {filename}')
    except KeyError as e:
        print(f'Please create environment variable: {e}')
    except TypeError as e:
        parser.print_help()

if __name__ == '__main__':
    main()
