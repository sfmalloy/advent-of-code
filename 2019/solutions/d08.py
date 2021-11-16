from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    ROWS = 6
    COLS = 25

    pixels = in_file.read().strip()
    layers = []
    min_zeros = float('inf')
    idx = ans_layer = 0
    while idx < len(pixels):
        layers.append(list(map(str, pixels[idx:idx + (ROWS*COLS)])))
        zeros = sum(map(lambda p:int(p == '0'), layers[-1]))
        if zeros < min_zeros:
            ans_layer = len(layers) - 1
            min_zeros = zeros
        idx += ROWS * COLS

    ones = 0
    twos = 0
    for p in layers[ans_layer]:
        ones += int(p == '1')
        twos += int(p == '2')
    print(ones * twos)

    for r in range(ROWS):
        for c in range(COLS):
            layer = 0
            pixel = r * COLS + c
            
            while layer < len(layers) and layers[layer][pixel] == '2':
                layer += 1
            layers[0][pixel] = layers[layer % len(layers)][pixel]
            print(u'\u2588' if layers[0][pixel] == '1' else ' ', end='')
        print()
