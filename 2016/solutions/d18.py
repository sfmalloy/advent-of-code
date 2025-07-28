from io import TextIOWrapper


def simulate(start: str, num_rows: int):
    row = [col == '^' for col in start]
    num_traps = len(row)-sum(row)
    for _ in range(num_rows-1):
        new_row = []
        check_row = [False]+row+[False]
        for i in range(1,len(check_row)-1):
            chunk = check_row[i-1:i+2]
            new_row.append((chunk[0] and chunk[1] and not chunk[2])
                or (chunk[1] and chunk[2] and not chunk[0])
                or (chunk[0] and not chunk[1] and not chunk[2])
                or (chunk[2] and not chunk[1] and not chunk[0]))
        num_traps += len(new_row)-sum(new_row)
        row = new_row
    return num_traps


def main(file: TextIOWrapper):
    start = file.read().strip()
    return simulate(start, 40), simulate(start, 400000)
