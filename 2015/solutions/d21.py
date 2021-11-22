from io import TextIOWrapper
from itertools import combinations
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Item:
    cost: int=0
    damage: int=0
    armor: int=0

@dataclass
class Creature:
    hp: int
    attack: int
    defense: int

    def take_damage(self, damage):
        self.hp -= damage - self.defense

def item_list(listing):
    return [(lambda i:Item(*map(int, i)))(w.split()) for w in listing.split('\n')]

def battle(weapon: Item, armor: Item, ring_a: Item, ring_b: Item, boss: Creature):
    me = Creature(100, weapon.damage + ring_a.damage + ring_b.damage, armor.armor + ring_a.armor + ring_b.armor)
    my_turn = True
    while me.hp > 0 and boss.hp > 0:
        if my_turn:
            boss.take_damage(me.attack)
        else:
            me.take_damage(boss.attack)
        my_turn = not my_turn

    return me.hp > 0

def main(in_file: TextIOWrapper):
    # yes I copied these from the website directly because I didn't want to type them myself
    weapons = item_list('''8     4       0
                           10     5       0
                           25     6       0
                           40     7       0
                           74     8       0''')

    armor = [Item()] + item_list('''13     0       1
                                    31     0       2
                                    53     0       3
                                    75     0       4
                                    102     0       5''')

    rings = [Item()] + item_list('''25     1       0
                                    50     2       0
                                    100     3       0
                                    20     0       1
                                    40     0       2
                                    80     0       3''')

    ring_dict = {r.cost: r for r in rings}
    ring_combos = list(sorted(list(map(lambda n:(n,0), [0,20,25,40,50,80,100])) + list((combinations([20,25,40,50,80,100], 2))), key=sum))

    boss = Creature(*(int(l.split(': ')[1]) for l in in_file.readlines()))

    min_cost = float('inf')
    max_cost = 0
    for w in weapons:
        for a in armor:
            for r in ring_combos:
                result = battle(w, a, ring_dict[r[0]], ring_dict[r[1]], deepcopy(boss))
                cost = w.cost + a.cost + ring_dict[r[0]].cost + ring_dict[r[1]].cost
                if result:
                    min_cost = min(min_cost, cost)
                else:
                    max_cost = max(max_cost, cost)

    print(min_cost)
    print(max_cost)
