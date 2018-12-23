#!/usr/bin/python

"""
"""

# 13:28 - 13:40
# Does not qualify - I cheated and looked this solution up so I could get the star

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

    def distance_p(self, position):
        return abs(self.position[0] - position[0]) + abs(self.position[1] - position[1]) + abs(self.position[2] - position[2])

    def is_in_range(self, position):
        return abs(self.position[0] - position[0]) + abs(self.position[1] - position[1]) + abs(self.position[2] - position[2]) <= self.radius

    def has_mutual_range_points(self, other):
        return self.distance(other) <= self.radius + other.radius

    def get_bounding_box(self):
        return BoundingBox(
            min_x = self.position[0] - self.radius,
            max_x = self.position[0] + self.radius,
            min_y = self.position[1] - self.radius,
            max_y = self.position[1] + self.radius,
            min_z = self.position[2] - self.radius,
            max_z = self.position[2] + self.radius,
            nanobots = [self])


class BoundingBox:
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z, nanobots):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z
        self.nanobots = nanobots

    def intersects(self, other):
        if self.min_x > other.max_x:
            return False
        elif self.max_x < other.min_x:
            return False
        elif self.min_y > other.max_y:
            return False
        elif self.max_y < other.min_y:
            return False
        elif self.min_z > other.max_z:
            return False
        elif self.max_z < other.min_z:
            return False
        else:
            return True

    def get_intersection(self, other):
        assert self.intersects(other)
        return BoundingBox(
            min_x=max(self.min_x, other.min_x),
            max_x=min(self.max_x, other.max_x),
            min_y=max(self.min_y, other.min_y),
            max_y=min(self.max_y, other.max_y),
            min_z=max(self.min_z, other.min_z),
            max_z=min(self.max_z, other.max_z),
            nanobots=self.nanobots + other.nanobots)

    def __repr__(self):
        return "Box(min_x=%s, max_x=%s, min_y=%s, max_y=%s, min_z=%s, max_z=%s, n_bots=%s)" % (self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z, len(self.nanobots))


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




def calc2(bots):
    #bots = get_bots(values)
    # FIX: Adding [0] to each range to make sure it's tested for
    xs = [x.position[0] for x in bots] + [0]
    ys = [x.position[1] for x in bots] + [0]
    zs = [x.position[2] for x in bots] + [0]

    dist = 1
    while dist < max(xs) - min(xs):
        dist *= 2

    while True:
        target_count = 0
        best = None
        best_val = None
        for x in range(min(xs), max(xs) + 1, dist):
            for y in range(min(ys), max(ys) + 1, dist):
                for z in range(min(zs), max(zs) + 1, dist):
                    count = 0
                    for bot in bots:
                        bx, by, bz = bot.position
                        bdist = bot.radius
                        if dist == 1:
                            calc = abs(x - bx) + abs(y - by) + abs(z - bz)
                            if calc <= bdist:
                                count += 1
                        else:
                            calc = abs(x / dist - bx / dist) + abs(y / dist - by / dist) + abs(z / dist - bz / dist)
                            if calc - 1 <= bdist / dist:
                                count += 1
                    if count > target_count:
                        target_count = count
                        best_val = abs(x) + abs(y) + abs(z)
                        best = (x, y, z)
                    elif count == target_count:
                        if best_val is None or abs(x) + abs(y) + abs(z) < best_val:
                            best_val = abs(x) + abs(y) + abs(z)
                            best = (x, y, z)

        if dist == 1:
            print("The max count I found was: " + str(target_count))
            return best, best_val
        else:
            xs = [best[0] - dist, best[0] + dist]
            ys = [best[1] - dist, best[1] + dist]
            zs = [best[2] - dist, best[2] + dist]
            # FIX: Python 3 changes how div works, we want integer math here
            dist = dist / 2

    


def main():
    nanobots = get_input()
    print calc2(nanobots)
    

if __name__ == "__main__":
    main()
