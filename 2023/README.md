# Advent of Code 2023

These solutions are written in Python 3, and some may use Python 3.12 features. You can run either a single day to get its answer and runtime, or run all the available days and get their combined runtime. This project is configured using `uv`.

## Commands

### Run single day
```
uv run main.py -d <day_number>
```

### Run all days
```
uv run main.py -a
```

### Other flags
```
-h, --help                          Show help message
-f <filepath>, --file <filepath>    Specify different input file from default
-n <number>, --numruns <number>     Specify number of runs to get an average time
-x, --hide                          Replace answer output with a bunch of X's
-i, --input                         Download/print input for day and do not run the solution
-g, --generate                      Generate template solution file for given day
```

## Dependencies
Most solutions use only the Python standard library (with the exception of Day 24 using `z3`). However, there are other dependencies for input downloading. To download them, simply run:
```
uv sync
```

## Solution Layout
New this year is a more dynamic way of adding solutions to be run. No longer do you have to modify `run.py` or anything to add new days to the runner. Instead, you simply import a global `advent` object (from the local `advent` module), and use a special decorator to mark your function as a solution.

Your solution function must accept 1 parameter which either is the file input of type `TextIOWrapper`, OR input parsed in a way that you define in a custom parser function (example below)
```py
from .lib.advent import advent
from io import TextIOWrapper


@advent.parser(1)
def day1_parser(file: TextIOWrapper):
    lines = file.readlines()
    return lines
```

There are 2 ways of writing solution functions. One way is if both your parts are contained in one function, you can return a tuple with the first value being the answer to part 1, and the second for part 2.

```py
from .lib.advent import advent
from io import TextIOWrapper


@advent.day(1)
def day1(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input and set return values
    return part1, part2
```

Another way is have seperate functions for parts 1 and 2. The input file gets reset between calls to part 1 and 2 functions, all you need to do is specify in the decorator what part each function is solving.

```py
from .lib.advent import advent
from io import TextIOWrapper


# you can choose to optionally write out `part=` if you want for clarity
@advent.day(1, part=1)
def day1_part1(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input and set part 1 return value
    return part1


@advent.day(1, 2)
def day1_part2(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input again and set part 2 return value
    return part2
```

## Solution Attributes
Part 2 functions can have some special attributes as well.

`use_part1: bool (default False)` - used for very specific scenarios when you want to use part 1's answer in the part 2 function.

```py
@advent.day(1, part=2, use_part1=True)
def solve2(ipt, part1_answer):
    # ...
```

`reparse: bool (default True)` - used to specify whether to run the parser function (if present) again between part 1 and part 2 functions (if both exist). If `False` and the parsed input is modified, those modifications will carry over to part 2 (assuming the input is mutable).

```py
@advent.day(1, part=2, reparsed=False)
def solve2(ipt):
    # ...
```
