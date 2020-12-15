import fileinput

nums = list(map(int, fileinput.input().readline().split(',')))

def play(nums, end):
  turns = {}
  last_spoken = 0
  for t in range(1, end+1):
    if t < len(nums)+1:
      # print(f'Turn {t}: Starting number {nums[t-1]}')
      turns[nums[t-1]] = (0, t)
      last_spoken = nums[t-1]
    elif turns[last_spoken][0] == 0:
      # print(f'Turn {t}: {last_spoken} spoken for the first time. Next is 0')
      last_spoken = 0
      turns[0] = (turns[0][1], t)
    else:
      # print(f'Turn {t}: {last_spoken} spoken before. Next is {turns[last_spoken][1]}-{turns[last_spoken][0]}={turns[last_spoken][1] - turns[last_spoken][0]}')
      last_spoken = turns[last_spoken][1] - turns[last_spoken][0]
      if last_spoken in turns:
        turns[last_spoken] = (turns[last_spoken][1], t)
      else:
        turns[last_spoken] = (0, t)
  return last_spoken

print(play(nums, 2020))
print(play(nums, 30000000))