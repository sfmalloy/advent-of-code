import fileinput

# Parse input
lines = [l.strip() for l in fileinput.input()]
rules_lines, cases = lines[:lines.index('')], lines[lines.index('')+1:]

# Turn rules into nested lists of ints
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

# Keeps track of current postition within string between function calls.
g_idx = 0

# check_str -> bool: Checks string to see if it is in the language defined by 'rules'
# 
# s: string to check
# rule_num: number of rule in 'rules' table. Defaults to 0 since 
#   that is what part 1 is looking for.
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
# Sum up all valid strings. No loops in language
ans = 0
for case in cases:
  g_idx = 0
  ans += check_str(case) and g_idx == len(case)
print(ans)

# Part 2
# Introduce loops into language, specifically rules 8 and 11.
rules[8] = [[42],[42,8]]
rules[11] = [[42,31],[42,11,31]]

# Rather than account for all combinations of anything, realize
#   that we only want some number of 8s followed by some number of 11s.
#
# In the loop I keep increasing the g_idx (within check_str) as long as the
#   substring up to g_idx follows rule 8. Once it follows both rule 8 and 11, 
#   return (as shown in the if statement) and the g_idx has reached the end of
#   the entire string, return. If it does not reach the end of the string or
#   goes past it, then the string is not in the recursive language.
ans = 0
for case in cases:
  g_idx = 0
  while check_str(case, 8):
    if check_str(case, 11) and g_idx == len(case):
      ans += 1
      break
print(ans)