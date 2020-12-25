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

card_loop = get_loop_size(7, card_public)
door_loop = get_loop_size(7, door_public)

print(get_key(door_public, card_loop))
