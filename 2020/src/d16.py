import fileinput
from copy import deepcopy

class field:
  def __init__(self, desc):
    self.name, range_desc = desc.split(': ')
    self.valid_entries = set()
    for r in range_desc.split(' or '):
      begin, end = map(int, r.split('-'))
      self.valid_entries |= set(i for i in range(begin, end+1))
  def valid(self, num):
    return num in self.valid_entries

lines = [l.strip() for l in fileinput.input()]
i = 0
fields = dict()
all_vals = set()
while lines[i] != '':
  f = field(lines[i])
  fields[f.name] = f
  all_vals |= f.valid_entries
  i += 1

i += 2
my_ticket = list(map(int, lines[i].split(',')))
i += 3

valid_tickets = []
invalid = 0
while i < len(lines):
  valid = True
  l = list(map(int, lines[i].split(',')))
  for n in l:
    if n not in all_vals:
      invalid += n
      valid = False
      break
  if valid:
    valid_tickets.append(l)
  i += 1
print(invalid)

cols = [[] for _ in range(len(fields))]

for t in valid_tickets:
  for i in range(len(fields)):
    cols[i].append(t[i])

possible = []
for c in cols:
  valid_fields = deepcopy(fields)
  for e in c:
    invalid = set()
    for f in valid_fields.values():
      if not f.valid(e):
        invalid.add(f.name)
    for inv in invalid:
      valid_fields.pop(inv)
  possible.append(list(valid_fields))

already_removed = set()
for _ in range(len(possible)):
  remove_name = ''
  for i in range(len(possible)):
    if len(possible[i]) == 1 and possible[i][0] not in already_removed:
      remove_name = possible[i][0]
      already_removed.add(remove_name)
      break
  for i in range(len(possible)):
    if len(possible[i]) > 1 and remove_name in possible[i]:
      possible[i].remove(remove_name)

p = 1
for n,e in zip(possible, my_ticket):
  if n[0][:(n[0].find(' '))] == 'departure':
    p *= e
print(p)