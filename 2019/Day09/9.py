from intcode import Intcode

p = list(map(int, open("9.in", 'r').read().strip().split(',')))

part1 = Intcode(p)
part2 = Intcode(p)

print("Part 1: %s" % part1.run([1])[0])
print("Part 2: %s" % part2.run([2])[0])
