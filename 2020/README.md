# Advent of Code 2020

These are my solutions to Advent of Code 2020 in Python. These were written running Python 3.8.5 specifically.

**Running**
----------------------------------
To run first move to the `src` directory by doing `cd src/`. Then do invoke one of three commands.

This runs a single day with default input file `(../inputs/dXY.in)`

    python run.py -d <day_number>

You can also add the `-f` flag followed by a file name/path to instead run with custom input.

    python run.py -d <day_number> -f <file>

Finally, you can run all days with their default inputs with the `-a` flag.

    python run.py -a

Each run prints the results for parts 1 and 2 respectively followed by the total runtime of both parts.
