import fileinput

lines = [l.strip() for l in fileinput.input()]
rules_lines, cases = lines[:lines.index('')], lines[lines.index('')+1:]

rules = {}

for r in rules_lines:
  num, definition = r.strip().split(': ')
  if definition[1] in 'ab':
    rules[int(num)] = definition[1]
  else:
    str_subdefs = definition.split(' | ')
    subdefs = []
    for sub in str_subdefs:
      subdef = []
      for sr in sub.split():
        subdef.append(int(sr))
      subdefs.append(subdef)
    rules[int(num)] = subdefs

g_idx = 0
def check_str(s, rule_num=0):
  global g_idx
  if rules[rule_num] == 'a' or rules[rule_num] == 'b':
    if g_idx >= len(s):
      return False
    valid = rules[rule_num] == s[g_idx]
    if valid:
      g_idx += 1
    return valid
  for r in rules[rule_num]:
    t = g_idx
    for sr in r:
      if not check_str(s, sr):
        g_idx = t
        break
    if g_idx != t:
      return True
  return False

# Part 1
ans = 0
for case in cases:
  g_idx = 0
  ans += check_str(case) and g_idx == len(case)
print(ans)

# Part 2
rules[8] = [[42],[42,8]]
rules[11] = [[42,31],[42,11,31]]

ans = 0
for case in cases:
  g_idx = 0
  while check_str(case, 8):
    temp_idx = g_idx
    if check_str(case, 11) and g_idx == len(case):
      ans += 1
      break
print(ans)