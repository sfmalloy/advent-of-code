import fileinput
from functools import reduce

groups = [g.rstrip().split('\n') for g in ''.join(fileinput.input()).split('\n\n')]

total = 0
yes = 0
for g in groups:
  unique = set()
  lines = []
  for l in g:
    line = set()
    for q in l:
      unique.add(q)
      line.add(q)
    lines.append(line)
  total += len(unique)
  unique = reduce(lambda x,y: x&y, lines)
  yes += len(unique)

print(total)
print(yes)
