import timeit
import os
import sys
import subprocess
from optparse import OptionParser

def num_file(num):
  if int(num) < 10:
    return f'0{num}'
  return num

def run(day):
  d = num_file(day)
  path = f'../inputs/d{d}.in'
  if not os.path.exists(path):
    print(f'File d{d}.in not found.')
    exit()
  if len(sys.argv) > 2:
    sys.argv.pop()
  t1 = timeit.default_timer()  
  subprocess.run(['python' , f'd{d}.py', path])
  t2 = timeit.default_timer()
  print(f'Time: {round(1000*(t2-t1),3)}ms')

def run_all():
  num = 1
  while os.path.exists(f'd{num_file(num)}.py'):
    print(f'Day {num}:')
    run(str(num))
    num += 1
    print()

parser = OptionParser()
parser.add_option('-d', '--day', dest='day', help='Run day <d>')
parser.add_option('-a', '--all', action='store_true', dest='run_all', 
  default=False, help='Run all days')

options, _ = parser.parse_args()

if options.run_all:
  run_all()
elif options.day is not None:
  run(options.day)