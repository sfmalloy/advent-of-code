import os
import sys
import subprocess

YEAR = '2020'
LANG = 'py'

if LANG == '':
	print('Please edit LANG varaible with desired programming language file extension.')
	exit()

argc = len(sys.argv)
argv = sys.argv

day_num = -1
if argc == 2:
	day_num = argv[1]
else:
	print('Please include day number. Exiting.')
	exit()

dir_name = 'Day' + ('0' if int(day_num) < 10 else '') + day_num

# Does this as safety not to override anything or spam requests to the site
dir_check = os.path.isdir(os.path.join(os.getcwd(), dir_name))
need_file_check = True
if not dir_check:
	subprocess.run(['mkdir', dir_name])
	need_file_check = False
if need_file_check:
	file_check = os.path.isfile(os.path.join(os.getcwd(), dir_name, f'{day_num}.in'))
	if file_check:
		print('Input already exists. Exiting.')
		exit()

if 'AOC_SESSION' in os.environ:
	AOC_SESSION = os.environ['AOC_SESSION']
	url = f'https://adventofcode.com/{YEAR}/day/{day_num}/input'

	print(f'Downloading Day {day_num}, Year {YEAR}')
	subprocess.run(['curl', '-o', os.path.join(os.getcwd(), dir_name, f'{day_num}.in'), url, '--cookie', f'session={AOC_SESSION}'], capture_output=True)
	print(f'Finished downloading')
	##### Feel free to change console commands between these comments to your liking.
	##### Syntax: subprocess.run(['cmd', args...])
	##### Use os.path.join(os.getcwd(), dir_name, ...) for any directory navigation

	# This creates file that you put your code in. Does not overwrite code if file exists.
	with open(os.path.join(os.getcwd(), dir_name, f'{day_num}.{LANG}'), 'a') as prog_file:
		os.utime(os.path.join(os.getcwd(), dir_name, f'{day_num}.{LANG}'), None)

	#####
else:
	print('AOC_SESSION not found. Please add session cookie as environment variable named AOC_SESSION.')