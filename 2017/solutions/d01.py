from lib import advent
from io import TextIOWrapper


@advent.parser(1)
def parse(file: TextIOWrapper) -> list[int]:
    return list(map(int, list(file.read().strip())))


@advent.solver(1)
def solve(nums: list[int]):
    p1 = 0
    p2 = 0
    N = len(nums)
    for i in range(N):
        near = nums[(i+1)%N]
        far = nums[(i+N//2)%N]
        p1 += near if nums[i] == near else 0
        p2 += far if nums[i] == far else 0
    
    return p1, p2
