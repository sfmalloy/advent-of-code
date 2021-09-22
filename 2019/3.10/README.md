# Advent of Code 2019
## Using Python 3.10

Pattern matching is here! So I decided to go back and revisit AoC 2019 to reimplement Intcode using features from Python 3.10. I also resolved other days as well just for fun. At the time of writing, the latest version of Python is Python 3.10rc2. To install it check out https://python.org/

To run a specific day:
```
python3.10 run.py -d <day_number>
```

You can also specify a file
```
python3.10 run.py -d <day_number> -f <path_to_file>
```

You can download your own input by running `download.py`. The input is automatically saved to the `inputs` folder. If you accidentally run `download.py` with the input file already existing, it won't make another get call as to not spam the site. If for whatever reason you want to redownload from the site, delete the input file and run the script. \(**Note:** you'll need a session cookie stored in an environment variable called AOC_SESSION, that is gotten from the Advent of Code website.\)
```
python3.10 download.py -d <day_number>
```
