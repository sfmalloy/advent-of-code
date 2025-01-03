from io import TextIOWrapper
from . import assembunny

def main(file: TextIOWrapper):
    lines = file.readlines()
    return assembunny.run(assembunny.parse(lines), [0, 0, 0, 0])[0], assembunny.run(assembunny.parse(lines), [0, 0, 1, 0])[0]
