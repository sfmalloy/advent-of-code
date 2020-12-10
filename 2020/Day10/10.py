from functools import lru_cache

with open('10.in') as f:
  adapters = [0] + sorted(int(a) for a in f.readlines())
  adapters.append(adapters[-1]+3)

# Part 1
diffs = [0,0,0,0]
for i in range(1, len(adapters)):
  diffs[adapters[i]-adapters[i-1]] += 1
print(diffs[1] * diffs[3])

# Part 2
@lru_cache
def count_valid(start):
  if start == 0:
    return 1
  total = 0
  idx = start-1
  while idx >= 0 and adapters[start]-adapters[idx] <= 3:
    total += count_valid(idx)
    idx -= 1
  return total
print(count_valid(len(adapters)-1))
