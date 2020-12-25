import fileinput

nums = list(map(int, fileinput.input().readline().split(',')))

def play(nums, end):
  prev_turns = {}
  turns = {}
  last_spoken = 0
  for t in range(1, end+1):
    if t < len(nums)+1:
      turns[nums[t-1]] = t
      prev_turns[nums[t-1]] = 0
      last_spoken = nums[t-1]
    elif prev_turns[last_spoken] == 0:
      last_spoken = 0
      prev_turns[0] = turns[0]
      turns[0] = t
    else:
      last_spoken = turns[last_spoken] - prev_turns[last_spoken]
      if last_spoken in turns:
        prev_turns[last_spoken] = turns[last_spoken]
        turns[last_spoken] = t
      else:
        prev_turns[last_spoken] = 0
        turns[last_spoken] = t
  return last_spoken

print(play(nums, 2020))
print(play(nums, 30000000))
