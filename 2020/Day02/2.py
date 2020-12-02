with open('2.in') as f:
  lines = [l.split() for l in f.readlines()]

valid1 = 0
valid2 = 0
for l in lines:
  min, max = map(int, l[0].split('-'))
  word = l[-1]
  letter = l[1][0]
  count = word.count(letter)
  valid1 += int(count >= min and count <= max)
  min -= 1
  max -= 1
  valid2 += word[min] != word[max] and (word[min] == letter or word[max] == letter)

print(valid1)
print(valid2)
