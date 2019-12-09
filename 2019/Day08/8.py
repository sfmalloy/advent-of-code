p = open("8.in",'r').readline().strip()
layer_size = 25 * 6

fewest_zero_start = 0
min_zeros = float("inf")
for i in range(0, len(p), layer_size):
    zeros = 0
    for j in range(i, i + layer_size):
        if (p[j] == '0'):
            zeros += 1
    if (zeros < min_zeros):
        fewest_zero_start = i
        min_zeros = zeros

ones = twos = 0
for i in range(fewest_zero_start, fewest_zero_start + layer_size):
    if (p[i] == '1'):
        ones += 1
    elif (p[i] == '2'):
        twos += 1

print(ones * twos)

image = [' '] * layer_size
for i in range(layer_size):
    for j in range(0, 100):
        index = i + (layer_size * j)
        if ((p[index] != '2') and image[i] == ' '):
            image[i] = p[index]

print_chr = {'0' : ' ', '1' : chr(9608)}
for i in range(layer_size):
    end_chr = '' if i % 25 != 24 else '\n'
    print(print_chr[image[i]], end=end_chr)
