from dataclasses import dataclass, field
from io import TextIOWrapper
from copy import deepcopy, copy

@dataclass
class Attack:
    mana: int=0
    dmg: int=0
    heal: int=0
    armor: int=0
    regen: int=0
    effect_idx: int=-1
    effect_turns: int=-1

@dataclass
class Player:
    hp: int=0
    mana: int=0
    armor: int=0
    effects: list[Attack]=field(default_factory=lambda:[None,None,None])

attacks = [
    Attack(mana=53, dmg=4),
    Attack(mana=73, dmg=2, heal=2),
    Attack(mana=113, effect_turns=6, effect_idx=0, armor=7),
    Attack(mana=173, effect_turns=6, effect_idx=1, dmg=3),
    Attack(mana=229, effect_turns=5, effect_idx=2, regen=101)
]

INF = float('inf')
# i may just be decreasing the limit until I got to "inf" as the final answer...
# it works. it's slow but it works
LIMIT = INF

def do_turn(player: Player, boss_hp: int, boss_dmg: int, mana_spent: int=0, player_turn: bool=True, hard: bool=False):
    if hard and player_turn:
        player.hp -= 1
        if player.hp <= 0:
            return INF
    if mana_spent >= LIMIT:
        return INF
    if boss_hp <= 0:
        return mana_spent

    # do effects
    if player.effects[0] is not None:
        player.effects[0].effect_turns -= 1
        player.armor = 7
        if player.effects[0].effect_turns == 0:
            player.effects[0] = None
    else:
        player.armor = 0
    
    if player.effects[1] is not None:
        player.effects[1].effect_turns -= 1
        boss_hp -= player.effects[1].dmg
        if player.effects[1].effect_turns == 0:
            player.effects[1] = None
    
    if player.effects[2] is not None:
        player.effects[2].effect_turns -= 1
        player.mana += player.effects[2].regen
        if player.effects[2].effect_turns == 0:
            player.effects[2] = None
    # end effects

    if boss_hp <= 0:
        return mana_spent

    best = INF
    if player_turn:
        for a in attacks:
            if player.mana - a.mana >= 0 and (a.effect_idx == -1 or player.effects[a.effect_idx] is None):
                new = deepcopy(player)
                new.mana -= a.mana
                new.hp += a.heal
                new_boss_hp = boss_hp
                if a.effect_idx >= 0:
                    new.effects[a.effect_idx] = copy(a)
                else:
                    new_boss_hp -= a.dmg
                best = min(best, do_turn(new, new_boss_hp, boss_dmg, mana_spent+a.mana, not player_turn, hard))
                if (LIMIT == INF and best != INF) or best < LIMIT:
                    return best
    elif boss_hp > 0:
        player.hp -= boss_dmg - player.armor
        if player.hp > 0:
            best = min(best, do_turn(player, boss_hp, boss_dmg, mana_spent, not player_turn, hard))
    elif boss_hp <= 0:
        return mana_spent

    return best

def main(in_file: TextIOWrapper):
    boss_hp = int(in_file.readline().split(':')[1])
    boss_dmg = int(in_file.readline().split(':')[1])
    player = Player(hp=50, mana=500)

    global LIMIT
    LIMIT = INF
    while True:
        curr = do_turn(deepcopy(player), boss_hp, boss_dmg)
        if curr == INF:
            break
        LIMIT = curr
    print(LIMIT)

    LIMIT = INF
    while True:
        curr = do_turn(deepcopy(player), boss_hp, boss_dmg, hard=True)
        if curr == INF:
            break
        LIMIT = curr
    print(LIMIT)
