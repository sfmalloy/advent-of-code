with open('1.in') as f:
  lines = [int(x) for x in f.readlines()]

for i in range(len(lines)):
  for j in range(i, len(lines)):
    if lines[i] + lines[j] == 2020:
      print(lines[i]*lines[j])

for i in range(len(lines)):
  for j in range(i, len(lines)):
    for k in range(j, len(lines)):
      if lines[i] + lines[j] + lines[k] == 2020:
        print(lines[i]*lines[j]*lines[k])