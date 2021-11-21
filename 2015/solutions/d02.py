from io import TextIOWrapper

def main(in_file: TextIOWrapper):
    paper = ribbon = 0
    for l,w,h in map(lambda l: map(int, l.strip().split('x')), in_file.readlines()):
        lw = l*w
        wh = w*h
        hl = h*l
        paper += 2*lw + 2*wh + 2*hl + min(lw,wh,hl)
        ribbon += 2*l + 2*w + 2*h - max(2*l, 2*w, 2*h) + l*w*h
    print(paper)
    print(ribbon)
