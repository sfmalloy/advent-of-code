import fileinput

lines = [l.strip().split() for l in fileinput.input()]

def run(replace=None, indices=[0]):
  other = 'jmp' if replace == 'nop' else 'nop'
  for i in indices:
    acc = 0
    ip = 0
    seen = set()
    looped = False
    if replace is not None:
      lines[i][0] = other
    while ip < len(lines):
      if ip in seen:
        looped = True
        if replace is not None:
          lines[i][0] = replace
        break
      seen.add(ip)
      v = int(lines[ip][1])
      if lines[ip][0] == 'jmp':
        ip += v
      else:
        if lines[ip][0] == 'acc':
          acc += v
        ip += 1
    if not looped or replace is None:
      return acc
  return None

print(run())

nops = []
jmps = []
for i in range(len(lines)):
  if lines[i][0] == 'nop':
    nops.append(i)
  elif lines[i][0] == 'jmp':
    jmps.append(i)

replace_nop = run('nop', nops)
replace_jmp = run('jmp', jmps)

if replace_nop is not None:
  print(replace_nop)
else:
  print(replace_jmp)