from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True, eq=True)
class LowHighInstruction:
    bot: int
    low_output: bool
    low: int
    high_output: bool
    high: int


def main(file: TextIOWrapper):
    prog_str = [line.strip() for line in file.readlines()]
    prog: set[LowHighInstruction] = set()
    chips = defaultdict(set)
    for line in prog_str:
        tokens = line.split()
        match tokens:
            case ['value', value, *_, bot]:
                chips[int(bot)].add(int(value))
            case ['bot', bot, _, _, _, low_type, low_id, _, _, _, high_type, high_id]:
                prog.add(LowHighInstruction(int(bot), low_type == 'output', int(low_id), high_type == 'output', int(high_id)))
    output = defaultdict(list)
    p1 = 0
    while len(prog) > 0:
        new_prog = set()
        for i in prog:
            if len(chips[i.bot]) == 2:
                if len(chips[i.bot] & {61, 17}) == 2:
                    p1 = i.bot
                mn = min(chips[i.bot])
                chips[i.bot].remove(mn)
                if i.low_output:
                    output[i.low].append(mn)
                else:
                    chips[i.low].add(mn)

                mx = max(chips[i.bot])
                chips[i.bot].remove(mx)
                if i.high_output:
                    output[i.high].append(mx)
                else:
                    chips[i.high].add(mx)
            else:
                new_prog.add(i)
        prog = new_prog

    return p1, output[0].pop()*output[1].pop()*output[2].pop()
