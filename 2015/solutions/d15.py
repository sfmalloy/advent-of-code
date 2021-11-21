from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class Ingredient:
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

def score_no_cal(ingredients: list[Ingredient], index, leftover, cap=0, dur=0, flv=0, txt=0):
    ing = ingredients[index]
    if index == len(ingredients) - 1:
        cap += ing.capacity * leftover
        dur += ing.durability * leftover
        flv += ing.flavor * leftover
        txt += ing.texture * leftover
        if any(map(lambda x: x<0, [cap,dur,flv,txt])):
            return 0
        return cap * dur * flv * txt

    mx = 0
    for i in range(leftover):
        mx = max(mx, score_no_cal(ingredients, index+1, leftover-i, cap + ing.capacity * i, dur + ing.durability * i, 
                                    flv + ing.flavor * i, txt + ing.texture * i))
    return mx

def score_cal(ingredients: list[Ingredient], index, leftover, cap=0, dur=0, flv=0, txt=0, cal=0):
    ing = ingredients[index]
    if index == len(ingredients) - 1:
        cap += ing.capacity * leftover
        dur += ing.durability * leftover
        flv += ing.flavor * leftover
        txt += ing.texture * leftover
        cal += ing.calories * leftover
        if any(map(lambda x: x<0, [cap,dur,flv,txt])) or cal != 500:
            return 0
        return cap * dur * flv * txt

    mx = 0
    for i in range(leftover):
        mx = max(mx, score_cal(ingredients, index+1, leftover-i, cap + ing.capacity * i, dur + ing.durability * i, 
                                flv + ing.flavor * i, txt + ing.texture * i, cal + ing.calories * i))
    return mx


def main(in_file: TextIOWrapper):
    ingredients: list[Ingredient] = []
    for line in in_file.readlines():
        l = ''.join(list(filter(lambda c: c.isdigit() or c in ',-', line)))
        ingredients.append(Ingredient(*map(int, l.split(','))))
    print(score_no_cal(ingredients, 0, 100))
    print(score_cal(ingredients, 0, 100))
