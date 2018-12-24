#!/usr/bin/python

"""
--- Day 24: Immune System Simulator 20XX ---
After a weird buzzing noise, you appear back at the man's cottage. He seems relieved to see his friend, but quickly notices that the little reindeer caught some kind of cold while out exploring.

The portly man explains that this reindeer's immune system isn't similar to regular reindeer immune systems:

The immune system and the infection each have an army made up of several groups; each group consists of one or more identical units. The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first and win ties), and sometimes weaknesses or immunities. Here is an example group:

18 units each with 729 hit points (weak to fire; immune to cold, slashing)
 with an attack that does 8 radiation damage at initiative 10
Each group also has an effective power: the number of units in that group multiplied by their attack damage. The above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one target. In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough units to actually receive all of that damage).

If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power; if there is still a tie, it chooses the defending group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target. Defending groups can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is being attacked by zero or one groups.

During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or the immune system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on the attacking group's attack type and the defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its effective power to the defending group. However, if the defending group is immune to the attacking group's attack type, the defending group instead takes no damage; if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.

The defending group only loses whole units from damage; damage is always dealt in such a way that it kills the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored. For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it loses exactly 7 units and is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army has lost all of its units.

For example, consider the following armies:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4
If these armies were to enter combat, the following fights, including details during the target selection and attacking phases, would take place:

Immune System:
Group 1 contains 17 units
Group 2 contains 989 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units
Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units
Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units
Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units
Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units
Immune System:
No groups remain.
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units
In the example above, the winning army ends up with 782 + 4434 = 5216 units.

You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now, how many units would the winning army have?
"""

from collections import defaultdict
from collections import deque

from functools import partial
import multiprocessing
import re
import sys
import time

ATTACK_TYPES = ['fire', 'cold', 'bludgeoning', 'slashing', 'radiation']

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

            print 'one attack:'
            print attacking_group.damage_type, defending_group.weaknesses
            print attacking_group.type, attacking_group.id, damage_dealt, defending_group.type, defending_group.id, units_killed
            print
            
            defending_group.unit_count -= units_killed
            assert defending_group.unit_count >= 0

        immune_system_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "IMMUNE_SYSTEM", units)))
        infection_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "INFECTION", units)))


        if immune_system_units == 0 or infection_units == 0:
            break
        
    immune_system_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "IMMUNE_SYSTEM", units)))
    infection_units = sum(map(lambda u: u.unit_count, filter(lambda u: u.type == "INFECTION", units)))        
    print "Immune system", immune_system_units, "Infection", infection_units

        
def main():
    units = get_input()
    run_fight(units)


if __name__ == "__main__":
    #print parse_weaknesses("immune to fire; weak to bludgeoning, slashing")
    main()
