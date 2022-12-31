from io import TextIOWrapper
from hashlib import md5


def main(file: TextIOWrapper):
    door_id = file.read().strip()
    pwd = ''
    end = 0
    while len(pwd) < 8:
        end += 1
        hashed = md5((door_id+str(end)).encode()).hexdigest()
        if hashed[:5] == '00000':
            pwd += hashed[5]

    epic_pwd = ['.'] * 8
    l = 0
    end = 0
    while l < 8:
        l = 0
        end += 1
        hashed = md5((door_id+str(end)).encode()).hexdigest()
        pos = int(hashed[5], 16)
        if hashed[:5] == '00000' and pos < 8 and epic_pwd[pos] == '.':
            l = 8
            epic_pwd[pos] = hashed[6]
            for p in epic_pwd:
                if p == '.':
                    l -= 1

    return pwd,''.join(epic_pwd)
