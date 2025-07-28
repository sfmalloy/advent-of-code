from io import TextIOWrapper
from intcode import Intcode
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class Packet:
    x: int
    y: int


def main(file: TextIOWrapper):
    prog = file.read()
    comps: list[Intcode] = []

    messages = defaultdict(deque[Packet])
    for addr in range(50):
        comps.append(Intcode(prog))
        comps[-1].read_in(addr)
    
    nat_sent: deque[Packet] = deque()
    p2 = 0
    while True:
        read_count = 0
        for i,comp in enumerate(comps):
            read = False
            while len(messages[i]) > 0:
                read = True
                packet = messages[i].popleft()
                comp.read_in(packet.x, packet.y)
            comp.read_in(-1)
            output = comp.read_out()
            for i in range(0, len(output), 3):
                dst, x, y = output[i:i+3]
                messages[dst].append(Packet(x, y))
            comp.run()
            if read:
                read_count += 1

        if read_count == 0 and len(messages[255]) > 0:
            msg = messages[255][-1]
            if len(nat_sent) > 0 and msg.y == nat_sent[-1].y:
                p2 = msg.y
                break
            messages[0].append(msg)
            nat_sent.append(msg)

    print(messages[255][0].y)
    print(p2)
