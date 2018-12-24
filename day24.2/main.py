#!/usr/bin/python

"""
--- Part Two ---
Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack damage. For example, if you were to boost the above example's immune system's units by 1570, the armies would instead look like this:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 6077 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 1595 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4
With this boost, the combat proceeds differently:

Immune System:
Group 2 contains 989 units
Group 1 contains 17 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 2 185832 damage
Infection group 1 would deal defending group 1 185832 damage
Infection group 2 would deal defending group 1 53820 damage
Immune System group 2 would deal defending group 1 1577455 damage
Immune System group 2 would deal defending group 2 1577455 damage
Immune System group 1 would deal defending group 2 206618 damage

Infection group 2 attacks defending group 1, killing 9 units
Immune System group 2 attacks defending group 1, killing 335 units
Immune System group 1 attacks defending group 2, killing 32 units
Infection group 1 attacks defending group 2, killing 84 units
Immune System:
Group 2 contains 905 units
Group 1 contains 8 units
Infection:
Group 1 contains 466 units
Group 2 contains 4453 units

Infection group 1 would deal defending group 2 108112 damage
Infection group 1 would deal defending group 1 108112 damage
Infection group 2 would deal defending group 1 53436 damage
Immune System group 2 would deal defending group 1 1443475 damage
Immune System group 2 would deal defending group 2 1443475 damage
Immune System group 1 would deal defending group 2 97232 damage

Infection group 2 attacks defending group 1, killing 8 units
Immune System group 2 attacks defending group 1, killing 306 units
Infection group 1 attacks defending group 2, killing 29 units
Immune System:
Group 2 contains 876 units
Infection:
Group 2 contains 4453 units
Group 1 contains 160 units

Infection group 2 would deal defending group 2 106872 damage
Immune System group 2 would deal defending group 2 1397220 damage
Immune System group 2 would deal defending group 1 1397220 damage

Infection group 2 attacks defending group 2, killing 83 units
Immune System group 2 attacks defending group 2, killing 427 units
After a few fights...

Immune System:
Group 2 contains 64 units
Infection:
Group 2 contains 214 units
Group 1 contains 19 units

Infection group 2 would deal defending group 2 5136 damage
Immune System group 2 would deal defending group 2 102080 damage
Immune System group 2 would deal defending group 1 102080 damage

Infection group 2 attacks defending group 2, killing 4 units
Immune System group 2 attacks defending group 2, killing 32 units
Immune System:
Group 2 contains 60 units
Infection:
Group 1 contains 19 units
Group 2 contains 182 units

Infection group 1 would deal defending group 2 4408 damage
Immune System group 2 would deal defending group 1 95700 damage
Immune System group 2 would deal defending group 2 95700 damage

Immune System group 2 attacks defending group 1, killing 19 units
Immune System:
Group 2 contains 60 units
Infection:
Group 2 contains 182 units

Infection group 2 would deal defending group 2 4368 damage
Immune System group 2 would deal defending group 2 95700 damage

Infection group 2 attacks defending group 2, killing 3 units
Immune System group 2 attacks defending group 2, killing 30 units
After a few more fights...

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 40 units

Infection group 2 would deal defending group 2 960 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 27 units
Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 13 units

Infection group 2 would deal defending group 2 312 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 13 units
Immune System:
Group 2 contains 51 units
Infection:
No groups remain.
This boost would allow the immune system's armies to win! It would be left with 51 units.

You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need to be cautious and find the smallest boost that would allow the immune system to win.

How many units does the immune system have left after getting the smallest boost it needs to win?
"""

from collections import defaultdict
from collections import deque

from functools import partial
import multiprocessing
import re
import sys
import time

GROUP_REGEX = re.compile(r"(\d+) units each with (\d+) hit points (\((.*)\) )?with an attack that does (\d+) (fire|cold|bludgeoning|slashing|radiation) damage at initiative (\d+)")

WEAKNESS_REGEX = re.compile(r"^weak to (.*)$")
IMMUNITIES_REGEX = re.compile(r"^immune to (.*)$")


class UnitGroup:
    def __init__(self, id, type, unit_count, hit_points, immunities, weaknesses, damage_count, damage_type, initiative):
        self.id = id
        self.type = type
        self.unit_count = unit_count
        self.hit_points = hit_points
        self.immunities = list(x.strip() for x in immunities)
        self.weaknesses = list(x.strip() for x in weaknesses)
        self.damage_count = damage_count
        self.damage_type = damage_type.strip()
        self.initiative = initiative

    def __repr__(self):
        return "%s %s" % (self.type, self.id)

    def effective_power(self):
        return self.unit_count * self.damage_count

    def damage_dealt_to(self, other):
        """
        Returns how much damage we would deal to other."""
        if self.damage_type in other.immunities:
            return 0
        multiplier = 2 if self.damage_type in other.weaknesses else 1
        return self.effective_power() * multiplier
    

def parse_weaknesses(weakness_string):
    weaknesses = []
    immunities = []

    if weakness_string is not None:
        tokens = weakness_string.split(";")        
        weakness_token = tokens[0].strip() if tokens[0].strip().startswith("weak to") else tokens[1].strip() if len(tokens) > 1 and tokens[1].strip().startswith("weak to") else None
        immunities_token = tokens[0].strip() if tokens[0].strip().startswith("immune to") else tokens[1].strip() if len(tokens) > 1 and tokens[1].strip().startswith("immune to") else None

        if weakness_token is not None:
            weaknesses = WEAKNESS_REGEX.match(weakness_token.strip()).groups()[0].split(", ")
        if immunities_token is not None:
            immunities = IMMUNITIES_REGEX.match(immunities_token.strip()).groups()[0].split(", ")
        
    return weaknesses, immunities


def boost_immune_system_units(units, boost):
    return map(
        lambda u: u if u.type == "INFECTION" else UnitGroup(
            id=u.id,
            type=u.type,
            unit_count=u.unit_count,
            hit_points=u.hit_points,
            immunities=u.immunities,
            weaknesses=u.weaknesses,
            damage_count=u.damage_count + boost,
            damage_type=u.damage_type,
            initiative=u.initiative),
        units)


def get_input():
    reading_immune_system = True
    unit_types = []
    id_count = 1
    try:
        while True:
            line = raw_input()
            if line == "Immune System:":
                continue
            elif line == "":
                continue
            elif line == "Infection:":
                reading_immune_system = False
                id_count = 1
                continue
            else:
                match = GROUP_REGEX.match(line)
                unit_count = int(match.groups()[0])
                hit_points = int(match.groups()[1])
                damage_count = int(match.groups()[4])
                damage_type = match.groups()[5]
                initiative = int(match.groups()[6])
                weaknesses, immunities = parse_weaknesses(match.groups()[3])
                type = 'IMMUNE_SYSTEM' if reading_immune_system else 'INFECTION'
                unit_types.append(UnitGroup(
                    id=id_count,
                    type=type,
                    unit_count=unit_count,
                    hit_points=hit_points,
                    immunities=immunities,
                    weaknesses=weaknesses,
                    damage_count=damage_count,
                    damage_type=damage_type,
                    initiative=initiative))
                id_count += 1

    except EOFError:
        return unit_types



def run_fight(units):
    while True:
        # By decreasing effective power, break ties with decreasing initiative
        units = sorted(units, key=lambda u: -u.initiative)
        units = sorted(units, key=lambda u: -u.effective_power())

        groups_chosen = []
        attack_mapping = {}

        # First, find targets
        for attacking_group in units:
            possible_defending_groups = filter(
                lambda u: u.type != attacking_group.type and attacking_group.damage_type not in u.immunities and u not in groups_chosen and u.unit_count > 0,
                units)
            if len(possible_defending_groups) == 0:
                continue

            # Highest damage, then highest effective power, then highest initiative
            possible_defending_groups = sorted(possible_defending_groups, key=lambda d: -d.initiative)
            possible_defending_groups = sorted(possible_defending_groups, key=lambda d: -d.effective_power())
            possible_defending_groups = sorted(possible_defending_groups, key=lambda d: -attacking_group.damage_dealt_to(d))

            target = possible_defending_groups[0]
            groups_chosen.append(target)

            attack_mapping[attacking_group] = target

        # Now, run the attacks
        attacking_groups = sorted(attack_mapping.keys(), key=lambda u: -u.initiative)
        for attacking_group in attacking_groups:
            if attacking_group.unit_count == 0:
                continue
            
            defending_group = attack_mapping[attacking_group]
            damage_dealt = attacking_group.damage_dealt_to(defending_group)
            units_killed = min(damage_dealt / defending_group.hit_points, defending_group.unit_count)

            defending_group.unit_count -= units_killed
            assert defending_group.unit_count >= 0

        immune_system_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "IMMUNE_SYSTEM", units)))
        infection_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "INFECTION", units)))

        if immune_system_units == 0 or infection_units == 0:
            break
        print immune_system_units, infection_units
        
    immune_system_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "IMMUNE_SYSTEM", units)))
    infection_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "INFECTION", units)))        

    if immune_system_units == 0:
        return False
    else:
        print "Immune system won!"
        print immune_system_units, infection_units
        return True

        
def main():
    base_units = get_input()

    # I just manually binary-searched for the value of '48' here
    units = boost_immune_system_units(base_units, 48)
    run_fight(units)

if __name__ == "__main__":
    main()
