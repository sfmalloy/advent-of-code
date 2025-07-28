from io import TextIOWrapper
from _md5 import md5
from functools import lru_cache


@lru_cache(maxsize=None)
def do_hash(ipt: str):
    return md5(ipt.encode()).hexdigest()


@lru_cache(maxsize=None)
def do_stretched_hash(ipt: str):
    curr = do_hash(ipt)
    for _ in range(2016):
        curr = do_hash(curr)
    return curr


def validate(salt: str, index: int):
    curr = do_hash(salt+str(index))
    for i in range(30):
        if curr[i] == curr[i+1] == curr[i+2]:
            for idx in range(index+1, index+1001):
                five = do_hash(salt+str(idx))
                for j in range(28):
                    if five[j] == curr[i] and five[j] == five[j+1] == five[j+2] == five[j+3] == five[j+4]:
                        return True
            return False
    return False


def validate_stretched(salt: str, index: int):
    curr = do_stretched_hash(salt+str(index))
    for i in range(30):
        if curr[i] == curr[i+1] == curr[i+2]:
            for idx in range(index+1, index+1001):
                five = do_stretched_hash(salt+str(idx))
                for j in range(28):
                    if five[j] == curr[i] and five[j] == five[j+1] == five[j+2] == five[j+3] == five[j+4]:
                        return True
            return False
    return False

def main(file: TextIOWrapper):
    salt = file.read().strip()
    index = 0
    keys = []
    while len(keys) < 64:
        if validate(salt, index):
            keys.append(index)
        index += 1
    
    index = 0
    stretched = []
    while len(stretched) < 64:
        if validate_stretched(salt, index):
            stretched.append(index)
        index += 1
    
    return keys[-1],stretched[-1]
