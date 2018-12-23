#!/usr/bin/python

"""
"""

# 13:28

from collections import defaultdict
from collections import deque

from functools import partial
import multiprocessing
import re
import sys
import time


REGEX = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")


class Nanobot:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def __repr__(self):
        return "Nanobot(position=%s, radius=%s)" % (self.position, self.radius)

    def distance(self, other):
        return abs(self.position[0] - other.position[0]) + abs(self.position[1] - other.position[1]) + abs(self.position[2] - other.position[2])


def get_input():
    result = []
    try:
        while True:
            match = REGEX.match(raw_input())
            result.append(Nanobot(
                position=(int(match.groups()[0]), int(match.groups()[1]), int(match.groups()[2])),
                radius=int(match.groups()[3])))
    except EOFError:
        return result


def main():
    nanobots = get_input()
    strongest = max(nanobots, key=lambda n: n.radius)

    for n in nanobots:
        print n
        
    print len(nanobots)
    print strongest
    
    print len(filter(lambda n: n.distance(strongest) <= strongest.radius, nanobots))

    #for nanobot in nanobots:
    #    print nanobot, nanobot.distance(strongest)


if __name__ == "__main__":
    main()
