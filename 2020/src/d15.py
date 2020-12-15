import fileinput
from collections import defaultdict

nums = list(map(int, fileinput.input().readline().split(',')))

def play(nums, end):
  turns = defaultdict(list)
  last_spoken = 0
  for t in range(1, end+1):
    if t < len(nums)+1:
      # print(f'Turn {t}: Starting number {nums[t-1]}')
      turns[nums[t-1]].append(t)
      last_spoken = nums[t-1]
    elif len(turns[last_spoken]) == 1:
      # print(f'Turn {t}: {last_spoken} spoken for the first time. Next is 0')
      last_spoken = 0
      turns[last_spoken].append(t)
    else:
      # print(f'Turn {t}: {last_spoken} spoken before. Next is {turns[last_spoken][-1]}-{turns[last_spoken][-2]}={turns[last_spoken][-1] - turns[last_spoken][-2]}')
      last_spoken = turns[last_spoken][-1] - turns[last_spoken][-2]
      turns[last_spoken].append(t)
  return last_spoken

print(play(nums, 2020))
print(play(nums, 30000000))