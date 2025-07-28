import fileinput
from collections import defaultdict, namedtuple

allergen_map = defaultdict(list)
total_counts = defaultdict(int)
lines = []
for line in fileinput.input():
  line = line.strip()
  food, allergens = line[:-1].split(' (contains ')
  food = food.split()
  allergens = allergens.split(', ')
  for a in allergens:
    for i in food:
      allergen_map[a].append(i)
  for i in food:
    total_counts[i] += 1
  lines.append((set(food), set(allergens)))

no_allergens = set()
yes_allergens = set()
for a,i_list in allergen_map.items():
  max_count = 0
  for i in i_list:
    max_count = max(max_count, i_list.count(i))
  actual = set()
  remove = set()
  for i in i_list:
    if i_list.count(i) == max_count:
      actual.add(i)
    else:
      remove.add(i)
  no_allergens |= remove
  yes_allergens |= actual

nope = no_allergens - yes_allergens
yep = yes_allergens - nope
print(sum(total_counts[i] for i in nope))

for a in allergen_map:
  allergen_map[a] = set(allergen_map[a]) - nope

new_allergen_map = defaultdict(set)
for a in allergen_map:
  new_ings = allergen_map[a].copy()
  for i in allergen_map[a]:
    for l in lines:
      if a in l[1]:
        if i not in l[0]:
          new_ings.remove(i)
          break
  new_allergen_map[a] = new_ings

complete = {}
printed = False
while len(complete) < len(new_allergen_map):
  to_remove = ''
  for k,v in new_allergen_map.items():
    if len(v) == 1 and k not in complete:
      to_remove = v.pop()
      complete[k] = to_remove
      break
  for a in new_allergen_map:
    if a != to_remove and to_remove in new_allergen_map[a]:
      new_allergen_map[a].remove(to_remove)

sort_map = {v:k for k,v in sorted(complete.items())}
lst = ''
for c in sort_map:
  lst += c + ','
print(lst[:-1])
