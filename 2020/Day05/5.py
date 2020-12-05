with open('5.in') as f:
  lines = f.readlines()

mseat = -float('inf')
ids = []
upper = 10000000
lower = 0
for l in lines:
  lo = 0
  hi = 127
  for i in range(7):
    if l[i] == 'F':
      hi = ((lo+hi)//2)-1
    else:
      lo = ((lo+hi)//2)+1
  row = lo
  lo = 0
  hi = 7
  for i in range(7, len(l)):
    if l[i] == 'L':
      hi = ((lo+hi)//2)
    else:
      lo = ((lo+hi)//2)
  col = hi
  curr_id = row*8+col
  mseat = max(mseat, curr_id)
  ids.append(curr_id)

print(mseat)

ids.sort()
for i in range(len(ids)-1):
  if ids[i+1] - ids[i] == 2:
    print(ids[i]+1)