from io import TextIOWrapper
from pprint import pprint
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True, eq=True)
class Ingredient:
    """Ingredient of a chemical reaction"""
    amount: int
    name: str

def count_ore(curr_name, amount_needed, reactions, curr_ore=0):
    if curr_name == 'ORE':
        return amount_needed
    res = reactions[curr_name][0]
    amount = res.amount
    if amount_needed > res.amount:
        amount *= amount_needed // res.amount
        if amount_needed % res.amount != 0:
            amount += 1
    
    total = 0
    for i in reactions[curr_name][1]:
        print(total, curr_ore)
        total += count_ore(i.name, amount * i.amount, reactions, total)
    return total

def main(in_file: TextIOWrapper):
    reactions = defaultdict(list)
    for line in in_file.readlines():
        recipe_str, result = line.strip().split(' => ')
        amt, name = result.split()
        reactions[name] = (Ingredient(int(amt), name), [(lambda a,b:Ingredient(int(a), b))(*r.split()) for r in recipe_str.split(', ')])
    print(count_ore('FUEL', 1, reactions))