from collections import defaultdict
from io import TextIOWrapper

def fill(nums: list[int], limit: int, curr_i: int=0, total: int=0, num_containers=0) -> tuple[int, defaultdict[int]]:
    container_counts = defaultdict(int)
    if total == limit:
        container_counts[num_containers] += 1
        return 1, container_counts
    if total > limit or curr_i == len(nums):
        return 0, container_counts

    count = 0
    for i in range(curr_i, len(nums)):
        c, cmap = fill(nums, limit, i+1, total+nums[i], num_containers+1)
        for k,v in cmap.items():
            container_counts[k] += v
        count += c
    return count, container_counts

def main(in_file: TextIOWrapper):
    containers = list(map(int, in_file.readlines()))
    total, count_map = fill(containers, 150)
    mn = float('inf')
    mn_combs = 0
    for k,v in count_map.items():
        if k < mn:
            mn_combs = v
            mn = k
    print(total)
    print(mn_combs)
