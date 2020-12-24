import fileinput

# Node class containing data and reference to next Node
class Node:
  def __init__(self, i_data=None, i_next=None):
    self.data = i_data
    self.next = i_next
  def set_next(self, new):
    self.next = new
  def __repr__(self):
    return str(self.data)

# Singly, circular linked list with a single reference to a Node.
class LinkedList:
  def __init__(self, data):
    self.size = 0
    self.head = Node(data[0])
    last = Node(data[-1], self.head)
    for i in range(1, len(data)-1):
      next_node = Node(data[i])
      self.head.set_next(next_node)
      self.head = next_node
    self.head.set_next(last)
  def insert_slice(self, ins_node, begin, size):
    end = begin
    for _ in range(size-1):
      end = end.next
    end.set_next(ins_node.next)
    ins_node.set_next(begin)
  def get_slice(self, prev, size):
    removed = []
    begin = prev.next
    end = begin
    for _ in range(size-1):
      removed.append(end.data)
      end = end.next
    removed.append(end.data)
    prev.set_next(end.next)
    end.set_next(None)
    return begin, removed
  def get_head(self):
    return self.head
  def step_forward(self):
    self.head = self.head.next

def play_round(cups: LinkedList, curr, nodes, mx):
  sliced, removed = cups.get_slice(curr, 3)
  dest_val = curr.data-1
  while dest_val < 1 or dest_val in removed:
    dest_val -= 1
    if dest_val < 1:
      dest_val = mx
  dest_node = nodes[dest_val]
  cups.insert_slice(dest_node, sliced, 3)

def play_game(data, rounds, mx):
  cups = LinkedList(data)
  nodes = [None for _ in range(len(data)+1)]
  for _ in range(len(data)):
    curr = cups.get_head()
    nodes[curr.data] = curr
    cups.step_forward()
  
  curr = nodes[data[0]]
  for _ in range(rounds):
    play_round(cups, curr, nodes, mx)
    curr = curr.next
  return nodes[1]

data = [int(cup) for cup in fileinput.input().readline().strip()]
mx1 = max(data)
game1 = play_game(data, 100, mx1)
not_one = game1.next
while not_one != game1:
  print(not_one, end='')
  not_one = not_one.next
print()

data += [i for i in range(mx1+1, 1000001)]
game2 = play_game(data, 10000000, 1000000)
print(game2.next.data * game2.next.next.data)