from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    gift_sue = set([
        ('children', 3),
        ('cats', 7),
        ('samoyeds', 2),
        ('pomeranians', 3),
        ('akitas', 0),
        ('vizslas', 0),
        ('goldfish', 5),
        ('trees', 3),
        ('cars', 2),
        ('perfumes', 1)
    ])
    gift_sue_dict = dict(gift_sue)
    sues = [set() for _ in range(500)]
    sue1 = (0,0)
    sue2 = (0,0)
    for i,sue in enumerate(in_file.readlines()):
        attrs = sue.rstrip().split(': ',1)[1].split(', ')
        for a in attrs:
            name,value = a.split(':')
            sues[i].add((name,int(value)))
        intersect = gift_sue.intersection(sues[i])
        if len(intersect) > sue1[0]:
            sue1 = (len(intersect),i+1)
        valid = 0
        for name,value in sues[i]:
            if ((name in {'cats','trees'} and value > gift_sue_dict[name])
                or (name in {'pomeranians','goldfish'} and value < gift_sue_dict[name])
                or (name not in {'cats','trees','pomeranians','goldfish'} and value == gift_sue_dict[name])):
                valid += 1
        if valid > sue2[0]:
            sue2 = (valid,i+1)

    print(sue1[1])
    print(sue2[1])
