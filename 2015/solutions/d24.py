from io import TextIOWrapper

best_depth = float('inf')
def least_qe(goal, idx, weights, total=0, qe=1, depth=0):
    global best_depth
    if depth > best_depth:
        return float('inf'), float('inf')
    if total == goal:
        best_depth = depth
        return qe, depth
    if idx < 0:
        return float('inf'), float('inf')
    best = (float('inf'), float('inf'))
    while idx >= 0:
        q, d = least_qe(goal, idx-1, weights, total+weights[idx], qe*weights[idx], depth+1)
        if d < best[1] or (d == best[1] and q < best[0]):
            best = (q, d)
        idx -= 1
    return best

def main(in_file: TextIOWrapper):
    global best_depth
    weights = list(reversed(list(map(int, in_file.readlines()))))
    group_weight = sum(weights) // 3
    print(least_qe(group_weight, len(weights) - 1, weights)[0])
    best_depth = float('inf')
    group_weight = sum(weights) // 4
    print(least_qe(group_weight, len(weights) - 1, weights)[0])
