from functools import reduce

with open('6.in') as f:
  groups = [g.rstrip().split('\n') for g in f.read().split('\n\n')]

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