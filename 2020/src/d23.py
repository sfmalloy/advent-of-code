import fileinput
from copy import deepcopy

class Node:
  def __init__(self, data=None, _prev=None, _next=None):
    self.data = data
    self.prev = _prev
    self.next = _next
  def __str__(self):
    return str(self.data)
  def __repr__(self):
    return str(self)
  def set_next(self, new):
    self.next = new
  def set_prev(self, new):
    self.prev = new
class DoublyLinkedList:
  def __init__(self):
    self.head = Node()
    self.head.set_next(self.head)
    self.head.set_prev(self.head)
    self.size = 0
  def insert_after(self, node, value):
    new = Node(value, _prev=node, _next=node.next)
    node.next.set_prev(new)
    node.set_next(new)    
    self.size += 1
  def insert_before(self, node, value):
    new = Node(value, _prev=node.prev, _next=node)
    node.prev.set_next(new)
    node.set_prev(new)
    self.size += 1
  def insert_end(self, value):
    self.insert_before(self.head, value)
  def insert_begin(self, value):
    self.insert_after(self.head, value)
  def get_next(self, node):
    if node.next == self.head:
      return self.head.next
    return node.next
  def get_prev(self, node):
    if node.prev == self.head:
      return self.head.prev
    return node.prev
  def get_slice(self, begin, size):
    nodes = []
    values = []
    for _ in range(size):
      t = self.get_next(begin)
      nodes.append(self.remove(begin))
      begin = t
      values.append(nodes[-1].data)
    for i in range(size):
      if i > 0:
        nodes[i].set_prev(nodes[i-1])
      if i < size-1:
        nodes[i].set_next(nodes[i+1])
    return nodes[0], values
  def insert_slice(self, dest_node, sliced_node):
    sliced_node.set_prev(dest_node)
    dest_old_next = dest_node.next
    dest_node.set_next(sliced_node)
    while sliced_node.next is not None:
      sliced_node = sliced_node.next
    dest_old_next.set_prev(sliced_node)
    sliced_node.set_next(dest_old_next)
  def remove(self, node):
    node.prev.set_next(node.next)
    node.next.set_prev(node.prev)
    node.set_next(None)
    node.set_prev(None)
    return node
  def walk(self):
    curr = self.head.next
    while curr != self.head:
      print(curr, end='->')
      curr = curr.next
    print()
  def walk_opp(self):
    curr = self.head.prev
    while curr != self.head:
      print(curr, end='->')
      curr = curr.prev
    print()


data = [int(cup) for cup in fileinput.input().readline().strip()]
mx = max(data)

cups = DoublyLinkedList()
number_to_node = {}
for d in data:
  cups.insert_end(d)
  number_to_node[d] = cups.head.prev

def play(cups, curr):
  sliced, removed = cups.get_slice(cups.get_next(curr), 3)
  dest_val = curr.data-1
  while dest_val < 1 or dest_val in set(removed):
    dest_val -= 1
    if dest_val < 1:
      dest_val = mx
  dest_node = number_to_node[dest_val]
  cups.insert_slice(dest_node, sliced)

curr = cups.get_next(cups.head)
for _ in range(100):
  play(cups, curr)
  curr = cups.get_next(curr)

one = cups.get_next(number_to_node[1])
while one.data != 1:
  print(one, end='')
  one = cups.get_next(one)
print()

cups = DoublyLinkedList()
number_to_node = {}

for d in data:
  cups.insert_end(d)
  number_to_node[d] = cups.head.prev
for i in range(mx+1, 1000001):
  cups.insert_end(i)
  number_to_node[i] = cups.head.prev
mx = 1000000

curr = cups.get_next(cups.head)
for i in range(10000000):
  play(cups, curr)
  curr = cups.get_next(curr)
a = cups.get_next(number_to_node[1])
b = cups.get_next(a)
print(a.data * b.data)