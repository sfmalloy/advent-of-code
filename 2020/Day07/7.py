from functools import lru_cache

color_map = {}
count_map = {}

with open('7.in') as f:
  rules = f.readlines()
  for r in rules:
    colors = r.strip('\n.').split(' bags contain ')
    if colors[1] != 'no other bags':
      color_map[colors[0]] = set((lambda c: (f'{c[1]} {c[2]}'))(color.split()) for color in colors[1].split(', '))
      count_map[colors[0]] = dict((lambda c: (f'{c[1]} {c[2]}', int(c[0])))(color.split()) for color in colors[1].split(', '))
    else:
      color_map[colors[0]] = None

@lru_cache(maxsize=None)
def count_outer(outer, goal):
  colors = {outer}
  if outer != goal and color_map[outer] is not None:
    for inner in color_map[outer]:
      subset = count_outer(inner, goal)
      colors |= subset
  if goal not in colors:
    return set()
  return colors

valid = set()
goal = 'shiny gold'
for c in color_map:
  valid |= count_outer(c, goal)
valid -= {goal}
print(len(valid))

def count_inner(outer, goal):
  count = 0
  if outer in count_map:
    for inner in color_map[outer]:
      count += count_map[outer][inner] + count_map[outer][inner]*count_inner(inner, goal)
  return count

print(count_inner(goal, goal))