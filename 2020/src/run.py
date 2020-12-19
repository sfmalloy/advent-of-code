import timeit
import os
import sys
from optparse import OptionParser

# Generate number with leading zero if less than 10
def num_file(num):
  if int(num) < 10:
    return f'0{num}'
  return num

# Run a single day given some file for input
def run_single(file, day):
  if not os.path.exists(file):
    print(f'File {file} not found.')
    exit()
  while len(sys.argv) > 2:
    sys.argv.pop()
  args = ['python', f'd{num_file(day)}.py', file]
  time = timeit.timeit(stmt=f'subprocess.run({args})', setup='import subprocess', number=1)
  print(f'Time: {round(1000*(time),3)}ms')

# Run every day with input file specified as ../inputs/d<day_number>.in
def run_all():
  num = 1
  fnum =  num_file(num)
  while os.path.exists(f'd{fnum}.py'):
    print(f'Day {num}:')
    run_single(f'../inputs/d{fnum}.in', num)
    num += 1
    fnum = num_file(num)
    print()

# Add command line options
parser = OptionParser()
parser.add_option('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '\
  'default uses input from inputs sibling directory.')
parser.add_option('-a', '--all', action='store_true', dest='run_all', 
  default=False, help='Run all days')
parser.add_option('-f', '--file', dest='file', help='')

options, _ = parser.parse_args()

if options.run_all:
  run_all()
elif options.day is not None:
  if options.file is not None:
    run_single(options.file, int(options.day))  
  else:
    run_single(f'../inputs/d{num_file(options.day)}.in', int(options.day))
