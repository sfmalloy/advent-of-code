with open('2.in') as f:
  lines = [l.split() for l in f.readlines()]

valid1 = 0
valid2 = 0
for l in lines:
  first, last = map(int, l[0].split('-'))
  word = l[-1]
  letter = l[1][0]
  count = word.count(letter)
  valid1 += count >= first and count <= last
  valid2 += word[first-1] != word[last-1] and letter in {word[first-1], word[last-1]}

print(valid1)
print(valid2)
