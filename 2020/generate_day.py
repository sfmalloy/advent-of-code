import os
import sys
import subprocess
import datetime

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

dir_name = 'inputs'
file_path = os.path.join(os.getcwd(), dir_name)

# Does this as safety not to override anything or spam requests to the site
dir_check = os.path.isdir(file_path)
need_file_check = True
if not dir_check:
	subprocess.run(['mkdir', dir_name])
	need_file_check = False
if need_file_check:
	file_check = os.path.isfile(os.path.join(file_path, f'd{day_num}.in'))
	if file_check:
		print('Input already exists. Exiting.')
		exit()

if 'AOC_SESSION' in os.environ:
	AOC_SESSION = os.environ['AOC_SESSION']
	URL = f'https://adventofcode.com/{YEAR}/day/{day_num}/input'

	# Downloads this day's input file as <day_num>.in
	if datetime.date.today() >= datetime.date(int(YEAR), 12, int(day_num)):
		print(f'Downloading Day {day_num}, Year {YEAR}')
		subprocess.run(['curl', '-o', os.path.join(file_path, f'd{day_num}.in'), URL, 
			'--cookie', f'session={AOC_SESSION}'], capture_output=True)
		print(f'Finished downloading')
	else:
		print(f'Too early to get input for day {day_num}')
else:
	print('AOC_SESSION not found. Please add session cookie as environment variable named AOC_SESSION.')