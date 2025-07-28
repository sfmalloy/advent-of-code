from io import TextIOWrapper


def main(file: TextIOWrapper):
    commands = file.readlines()
    print(shuffle(commands, 10007, 2019))

    # https://www.reddit.com/r/adventofcode/comments/etxg0o/how_do_i_solve_day_22_part_2_2019_x_times_in_a_row/
    # needed this hint and I STILL took 2 days to solve this lol
    N = 119315717514047
    iters = 101741582076661
    pos = 2020

    pos0 = shuffle_inverse(commands, N, 0)
    pos1 = shuffle_inverse(commands, N, 1)
    b0 = pos0
    m0 = (pos1 - pos0) % N

    m = pow(m0, iters, N) % N
    ba = (1 - pow(m0, iters, N)) % N
    bb = mod_inverse(1 - m0, N)
    b = b0 * ba * bb
    print((b + m*pos) % N)


def shuffle(commands: list[str], N: int, pos: int):
    for cmd in commands:
        words = cmd.split()
        match words:
            case ['cut', x]:
                pos = cut(pos, int(x), N)
            case ['deal', 'into', 'new', 'stack']:
                pos = new_stack(pos, N)
            case ['deal', 'with', 'increment', x]:
                pos = deal(pos, int(x), N)
    return pos


def shuffle_inverse(commands: list[str], N: int, pos: int):
    for cmd in reversed(commands):
        words = cmd.split()
        match words:
            case ['cut', x]:
                pos = inverse_cut(pos, int(x), N)
            case ['deal', 'into', 'new', 'stack']:
                pos = new_stack(pos, N)
            case ['deal', 'with', 'increment', x]:
                pos = inverse_deal(pos, int(x), N)
    return pos


def new_stack(pos: int, N: int) -> int:
    return -(pos + 1) % N


def cut(pos: int, x: int, N: int) -> int:
    if x < 0:
        x += N
    return (pos + (N - x)) % N


def deal(pos: int, x: int, N: int) -> int:
    return (pos * x) % N


def inverse_cut(pos: int, x: int, N: int) -> int:
    if x < 0:
        x += N
    return (pos + x) % N


def inverse_deal(pos: int, x: int, N: int) -> int:
    return (pos * mod_inverse(x, N)) % N


# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def mod_inverse(a, n):
    # took days for me to realize I needed these 2 lines :)
    if a < 0:
        a %= n

    t = 0
    new_t = 1
    r = n
    new_r = a

    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t-q*new_t
        r, new_r = new_r, r-q*new_r

    if t < 0:
        t += n
    return t
