#!/usr/bin/python

"""
"""

from collections import defaultdict
from collections import deque

from functools import partial
import multiprocessing
import re
import sys
import time


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])


def can_merge(lhs, rhs):
    for p_lhs in lhs:
        for p_rhs in rhs:
            if dist(p_rhs, p_lhs) <= 3:
                return True
    return False


def count_constellations(points):
    # Ya this is embarrassing
    constellations = list([x] for x in points)
    for idx in range(len(constellations)):
        for jdx in range(len(constellations)):
            if idx == jdx:
                continue
            if can_merge(constellations[idx], constellations[jdx]):
                constellations[idx] = constellations[idx] + constellations[jdx]
                constellations[jdx] = []

    constellations = list(filter(lambda c: len(c) > 0, constellations))
    for idx in range(len(constellations)):
        for jdx in range(len(constellations)):
            if idx == jdx:
                continue
            if can_merge(constellations[idx], constellations[jdx]):
                constellations[idx] = constellations[idx] + constellations[jdx]
                constellations[jdx] = []

    constellations = list(filter(lambda c: len(c) > 0, constellations))
    for idx in range(len(constellations)):
        for jdx in range(len(constellations)):
            if idx == jdx:
                continue
            if can_merge(constellations[idx], constellations[jdx]):
                constellations[idx] = constellations[idx] + constellations[jdx]
                constellations[jdx] = []                
    
    return len(filter(lambda c: len(c) > 0, constellations))


def get_input():
    result = []
    try:
        while True:
            result.append(tuple(list(int(x) for x in raw_input().split(","))))
        pass
    except EOFError:
        return result

        
def main():
    points = get_input()

    print count_constellations(points)


if __name__ == "__main__":
    main()
