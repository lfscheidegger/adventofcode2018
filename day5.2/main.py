#!/usr/bin/python

"""
--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

from collections import defaultdict

import multiprocessing
import re
import sys

        
def get_input():
    return raw_input()

def all_units(polymer):
    return set(x.lower() for x in polymer)

def polymer_without_unit(polymer, unit):
    return filter(lambda x: x.lower() != unit.lower(), polymer)

def reduce_polymer(polymer):
    for idx in range(len(polymer) - 1):
        v0 = polymer[idx]
        v1 = polymer[idx+1]
        case_match = (v0.islower() and not v1.islower()) or (v1.islower() and not v0.islower())
        value_match = v0.lower() == v1.lower()
        if case_match and value_match:
            # found a reduction - do it
            return polymer[:idx] + polymer[idx+2:]

    # no reduction possible
    return polymer

def try_reduce(data):
    unit, polymer = data
    print unit
    while True:
        size = len(polymer)
        polymer = reduce_polymer(polymer)
        new_size = len(polymer)
        if size == new_size:
            break
    return len(polymer)

def main():
    polymer = get_input()
    units = all_units(polymer)
    smallest_reduction = len(polymer) + 1

    data = []
    
    for unit in units:
        filtered_polymer = polymer_without_unit(polymer, unit)
        data.append((unit, filtered_polymer))

    p = multiprocessing.Pool(processes=8)
    print min(list(p.map(try_reduce, data)))
        #smallest_reduction = min(smallest_reduction, try_reduce(filtered_polymer))

    # print smallest_reduction
    
if __name__ == "__main__":
    main()
