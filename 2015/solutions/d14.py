from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class Reindeer:
    speed: int
    speed_time: int
    rest_time: int
    
    is_resting: bool = False
    timer: int = 0
    dist: int = 0
    score: int = 0

def main(in_file: TextIOWrapper):
    reindeer: list[Reindeer] = []
    for l in in_file.readlines():
        data = l.strip().split()
        reindeer.append(Reindeer(int(data[3]), int(data[6]), int(data[13])))
    
    T = 2503
    for _ in range(T):
        lead = 0
        lead_dist = 0
        for i, r in enumerate(reindeer):
            if r.is_resting:
                if r.timer < r.rest_time:
                    r.timer += 1
                else:
                    r.timer = 0
                    r.is_resting = False

            if not r.is_resting:
                if r.timer < r.speed_time:
                    r.timer += 1
                    r.dist += r.speed
                else:
                    r.timer = 1
                    r.is_resting = True
            if r.dist > lead_dist:
                lead_dist = r.dist
                lead = i
        reindeer[lead].score += 1

    mx_dist = 0
    mx_score = 0
    for r in reindeer:
        mx_dist = max(r.dist, mx_dist)
        mx_score = max(r.score, mx_score)
    print(mx_dist)
    print(mx_score)
