import fileinput

lines = [int(x) for x in fileinput.input()]

N = 25
invalid = 0
preamble = lines[:N]
for i in range(N, len(lines)):
  found = False
  for a in range(len(preamble)):
    for b in range(a+1, len(preamble)):
      if preamble[a]+preamble[b] == lines[i]:
        found = True
        break
    if found:
      break
  if not found:
    invalid = lines[i]
    break
  preamble.pop(0)
  preamble.append(lines[i])
print(invalid)

sumlist = []
s = 0
for i in range(len(lines)):
  if s < invalid:
    sumlist.append(lines[i])
    s += lines[i]
  elif s == invalid:
    break
  while s > invalid:
    s -= sumlist.pop(0)

print(min(sumlist) + max(sumlist))