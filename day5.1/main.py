#!/usr/bin/python

"""
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
