from intcode import Intcode

p = list(map(int, open("5.in", 'r').read().strip().split(',')))
part1 = Intcode(p)
part2 = Intcode(p)

print(part1.run([1])[-1])
print(part2.run([5])[0])
