#!/usr/bin/python

"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)
"""

from collections import defaultdict

import re
import sys

        
def get_input():
    return raw_input()

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

def main():
    polymer = get_input()
    size = len(polymer)
    while True:
        size = len(polymer)
        polymer = reduce_polymer(polymer)
        new_size = len(polymer)
        print "Reduced:", new_size
        if size == new_size:
            break
    print len(polymer)
    
if __name__ == "__main__":
    main()
