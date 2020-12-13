import fileinput

earliest, buses = fileinput.input()
earliest = int(earliest)
buses = [int(b) if b != 'x' else 0 for b in buses.split(',')]
earliest_bus = (float('inf'), 0)
running = {}
idx = 0
prod = 1
for b in buses:
  if b > 0:
    running[b] = idx
    prod *= b
    t = 0
    while t < earliest:
      t += b
    if earliest_bus[0] > t:
      earliest_bus = (t, b)
  idx += 1
print(earliest_bus[1]*(earliest_bus[0]-earliest))

def mod_inv(a, n):
  p = 0
  while (p*a) % n != 1:
    p += 1
  return p

t = 0
for bus in running:
  t += ((bus-running[bus])*(prod//bus)*mod_inv(prod/bus, bus))
t %= prod
print(t)
