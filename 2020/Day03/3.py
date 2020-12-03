with open('3.in') as f:
  lines = [[c for c in line.strip()] for line in f.readlines()]

def count_trees(dx, dy):
  x = 0
  count = 0
  for y in range(0, len(lines), dy):
    if x >= len(lines[0]):
      x %= len(lines[0])
    if lines[y][x] == '#':
      count += 1
    x += dx
  return count

p = 1
pairs = [(1,1),(3,1),(5,1),(7,1),(1,2)]
for dx,dy in pairs:
  count = count_trees(dx,dy)
  p *= count

print(count_trees(3,1))
print(p)