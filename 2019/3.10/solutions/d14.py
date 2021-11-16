from io import TextIOWrapper
from math import ceil
from collections import namedtuple

ing = namedtuple('ing', 'need name')

class recipe:
  # product given as 
  #   <int> <name>
  # ingredients given as list of
  #   <int> <name>
    def __init__(self, recipe):

        ingredients, product = recipe.split(' => ')

        product = product.split()
        self.amt = int(product[0])
        self.name = product[1]

        ingredients = ingredients.split(', ')
        self.inputs = [(lambda s: ing(int(s[0]), s[1]))(i.split()) for i in ingredients]

def get_ore(num_fuel, cookbook, base_chems):
    ore_count = 0
    leftovers = {i:0 for i in cookbook}
    frontier = [ing(num_fuel, 'FUEL')]
    while len(frontier) > 0:
    # generate future moves
        f = frontier.pop(0)
        ratio = ceil(f.need / cookbook[f.name].amt)

        added_nonbase = []
        added_base = []
        if f.name not in base_chems:
            for i in cookbook[f.name].inputs:
                diff = ratio * i.need - leftovers[i.name]
                if i.name in base_chems:
                    added_base.append(ing(diff, i.name))
                else:
                    added_nonbase.append(ing(diff, i.name))
                leftovers[i.name] = 0
            frontier = added_nonbase + added_base + frontier
        else:
            if leftovers[f.name] > 0:
                ratio = ceil((f.need - leftovers[f.name]) / cookbook[f.name].amt)
            ore_count += cookbook[f.name].inputs[0].need * ratio
        leftovers[f.name] += cookbook[f.name].amt * ratio - f.need
    return ore_count

def main(in_file: TextIOWrapper):
    r_objs = [recipe(l.rstrip()) for l in in_file.readlines()]
    cookbook = {r.name:r for r in r_objs}
    base_chems = set()
    for c in cookbook:
        if cookbook[c].inputs[0].name == 'ORE':
            base_chems.add(c)
    
    total_ore = 1000000000000

    print(get_ore(1, cookbook, base_chems))

    # slightly faster brute forcing
    fuel = 1
    while total_ore - get_ore(fuel, cookbook, base_chems) > 0:
        fuel += 1024

    while total_ore - get_ore(fuel, cookbook, base_chems) < 0:
        fuel -= 1

    print(fuel)


