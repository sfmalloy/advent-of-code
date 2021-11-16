import time
with open('16.in') as rf:
  line = rf.readline().rstrip()
  digits = list(map(int, map(str, line)))
  real_digits = digits.copy() * 10000

def do_pattern(nums, pos):
  i = pos
  step = 2*(pos+1)
  rep = 1
  d = 0
  while i < len(nums):
    for n in nums[i:i+pos+1]:
      d += n * rep
    i += step
    rep *= -1
  return abs(d) % 10

phases = 100
for _ in range(phases):
  digits = [do_pattern(digits, i) for i in range(len(digits))]

[print(d, end='') for d in digits[:8]]
print()

skip = 0
pow10 = 1
for s in real_digits[6::-1]:
  skip += pow10 * s
  pow10 *= 10

real_digits = real_digits[skip:]
for k in range(phases):
  new_real = []
  s = sum(real_digits)
  for i in range(len(real_digits)):
    new_real.append(s % 10)
    s -= real_digits[i]
  real_digits = new_real
[print(d, end='') for d in real_digits[:8]]
print()