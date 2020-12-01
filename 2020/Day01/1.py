with open('1.in') as f:
  l = sorted(map(int, f.readlines()))

def find_sum(l, n, d, p=0, s=0):
  if s > n:
    return 0
  if d == 0:
    return int(s == n)
  for i in range(p, len(l)):
    prod = l[i] * find_sum(l, n, d-1, i+1, s+l[i])
    if prod > 0:
      return prod
  return 0

print(find_sum(l, 2020, 2))
print(find_sum(l, 2020, 3))