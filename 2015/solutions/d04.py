from io import TextIOWrapper
from hashlib import md5

def leading_zeros_hash(key, num_zeros):
    num = 0
    zeros = '0' * num_zeros
    # Yeah I'm not implementing md5 from scratch...thank you Python std lib.
    while md5(bytes(f'{key}{num}', 'utf-8')).hexdigest()[0:num_zeros] != zeros:
        num += 1
    return num

def main(in_file: TextIOWrapper):
    key = in_file.readline().strip()
    print(leading_zeros_hash(key, 5))
    print(leading_zeros_hash(key, 6))
