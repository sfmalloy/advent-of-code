import fileinput
from collections import deque
from itertools import islice

lines = [l.strip() for l in fileinput.input()]

p1 = deque(map(int, lines[1:lines.index('')]))
p2 = deque(map(int, lines[lines.index('')+2:]))

p1_rec = p1.copy()
p2_rec = p2.copy()

i = 0
while len(p1) > 0 and len(p2) > 0:
  card1 = p1.popleft()
  card2 = p2.popleft()
  if card1 > card2:
    p1.append(card1)
    p1.append(card2)
  else:
    p2.append(card2)
    p2.append(card1)
  
winner = p1 if len(p1) > len(p2) else p2
print(sum(winner[i]*(len(winner)-i) for i in range(len(winner))))

def rec_crab(p1, p2):
  seen = set()
  while len(p1) > 0 and len(p2) > 0:
    if (tuple(p1), tuple(p2)) in seen:
      return 1
    seen.add((tuple(p1), tuple(p2)))

    card1 = p1.popleft()
    card2 = p2.popleft()

    if card1 <= len(p1) and card2 <= len(p2):
      sub_winner = rec_crab(deque(islice(p1.copy(), 0, card1)), deque(islice(p2.copy(), 0, card2)))
    elif card1 > card2:
      sub_winner = 1
    else:
      sub_winner = 2
    
    if sub_winner == 1:
      p1.append(card1)
      p1.append(card2)
    else:
      p2.append(card2)
      p2.append(card1)
  return 1 if len(p1) > len(p2) else 2

winner_rec = p1_rec if rec_crab(p1_rec, p2_rec) == 1 else p2_rec
print(sum(winner_rec[i]*(len(winner_rec)-i) for i in range(len(winner_rec))))
