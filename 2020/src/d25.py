import fileinput

card_public, door_public = map(int, fileinput.input())

def transform(val, subject):
  return (val*subject) % 20201227

def get_loop_size(subject, goal):
  loop = 0
  val = 1
  while val != goal:
    val = transform(val, subject)
    loop += 1
  return loop

def get_key(subject, loop_size):
  val = 1
  for _ in range(loop_size):
    val = transform(val, subject)
  return val

# To get faster run time (assuming the answer is correct)
#   comment out one of door_loop or card_loop and then
#   the other key (so if you comment out door_loop, comment
#   out card_key). They're both here to show correctness.
door_loop = get_loop_size(7, door_public)
card_loop = get_loop_size(7, card_public)

card_key = get_key(card_public, door_loop)
door_key = get_key(door_public, card_loop)

if card_key == door_key:
  print(door_key)
