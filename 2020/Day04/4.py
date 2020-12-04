with open('4.in') as f:
  lines = f.readlines()

def is_valid2_entry(k,v):
  if k == 'byr':
    v = int(v)
    return 1920 <= v <= 2002
  elif k == 'iyr':
    v = int(v)
    return 2010 <= v <= 2020
  elif k == 'eyr':
    v = int(v)
    return 2020 <= v <= 2030
  elif k == 'hgt':
    if len(v) <= 2:
      return False
    else:
      unit = v[-2:]
      v = int(v[:-2])
      if unit == 'cm' and not (150 <= v <= 193):
        return False
      elif unit == 'in' and not (59 <= v <= 76):
        return False
      elif unit not in ['cm','in']:
        return False
  elif k == 'hcl':
    if v[0] != '#' or len(v) != 7:
      return False
    for c in v[1:]:
      if c not in '0123456789abcdef':
        return False
  elif k == 'ecl':
    return v in {'amb','blu','brn','gry','grn','hzl','oth'}
  elif k == 'pid':
    if len(v) != 9:
      return False
    for d in v:
      if d not in '0123456789':
        return False
  return True

valid1 = 0
valid2 = 0
curr = []
for l in lines:
  if l != '\n':
    curr += l.split()
  if l == '\n' or l == lines[-1]:
    found = 0
    found_cid = False
    for field in curr:
      if field[:3] != 'cid':
        found += 1
      else:
        found_cid = True
        break
    if len(curr) == 8 or (found == 7 and not found_cid):
      valid1 += 1
      is_valid2 = True
      for entry in curr:
        k,v = entry.split(':')
        is_valid2 = is_valid2_entry(k,v)
        if not is_valid2:
          break
      if is_valid2:
        valid2 += 1
    curr = []
print(valid1)
print(valid2)
