#!/usr/bin/python

"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

from collections import defaultdict

import multiprocessing
import re
import sys


class Anchor:
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords
        self.owned_count = 0

    def __repr__(self):
        return "Point(id=%d, coords=%s)" % (self.id, self.coords)


class GridPoint:
    def __init__(self, owners, distance, coords):
        self.owners = owners
        self.distance = distance
        self.coords = coords
        self.is_tied = False


class Grid:
    def __init__(self, grid_points, min_x, max_x, min_y, max_y):
        self.grid_points = grid_points
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def print_grid(self):
        for y in range(self.min_y, self.max_y+1):
            line = []
            for x in range(self.min_x, self.max_x+1):
                grid_point = self.grid_points[(x, y)]
                if grid_point.owners == []:
                    line.append('-')
                elif len(grid_point.owners) > 1:
                    line.append('.')
                elif grid_point.distance == 0:
                    line.append(chr(grid_point.owners[0].id + ord('A')))
                else:
                    assert len(grid_point.owners) == 1
                    line.append(chr(grid_point.owners[0].id + ord('a')))

            print ''.join(line)                    


def manhattan_distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


def fill_grid(grid, points):
    for point in points:
        for grid_point_coords in grid.grid_points:
            grid_point = grid.grid_points[grid_point_coords]
            distance = manhattan_distance(grid_point.coords, point.coords)
            if len(grid_point.owners) == 0 or grid_point.distance > distance:
                for old_point in grid_point.owners:
                    if len(grid_point.owners) == 1:
                        old_point.owned_count -= 1
                    if old_point.owned_count < 0:
                        old_point.owned_count = 0
                grid_point.owners = [point]
                point.owned_count += 1
                grid_point.distance = distance
                
            elif grid_point.distance == distance:
                for old_point in grid_point.owners:
                    if len(grid_point.owners) == 1:
                        old_point.owned_count -= 1
                    if old_point.owned_count < 0:
                        old_point.owned_count = 0
                grid_point.owners.append(point)

                
def build_grid(min_x, min_y, max_x, max_y, border=2):
    result = {}
    for x in range(min_x-border, max_x+border+1):
        for y in range(min_y-border, max_y+border+1):
            result[(x, y)] = GridPoint(owners=[], distance=-1, coords=(x, y))

    return Grid(grid_points=result, min_x=min_x-border, max_x=max_x+border, min_y=min_y-border, max_y=max_y+border)


def get_infinite_region_ids(grid):
    result = set()
    for grid_point_coords in grid.grid_points:
        grid_point = grid.grid_points[grid_point_coords]
        if grid_point_coords[0] == grid.min_x or \
           grid_point_coords[0] == grid.max_x or \
           grid_point_coords[1] == grid.min_y or \
           grid_point_coords[1] == grid.max_y:
            if len(grid_point.owners) == 1:
                result = result.union(set(list(x.id for x in grid_point.owners)))

    return result


def get_raw_input():
    result = []
    try:
        idx = 0
        while True:
            x, y = raw_input().split(", ")
            result.append((idx, int(x), int(y)))
            idx += 1
    except EOFError:
        return result

        
def get_input():
    result = []
    try:
        idx = 0
        while True:
            x, y = raw_input().split(", ")
            result.append(Anchor(idx, (int(x), int(y))))
            idx += 1

    except EOFError:
        return result


def main():
    raw_data = get_raw_input()
    small_points = list(Anchor(id=l[0], coords=(l[1], l[2])) for l in raw_data)
    # big_points = list(Anchor(id=l[0], coords=(l[1], l[2])) for l in raw_data)

    min_x = min(small_points, key=lambda x: x.coords[0]).coords[0]
    min_y = min(small_points, key=lambda x: x.coords[1]).coords[1]

    max_x = max(small_points, key=lambda x: x.coords[0]).coords[0]
    max_y = max(small_points, key=lambda x: x.coords[1]).coords[1]

    grid = build_grid(min_x, min_y, max_x, max_y)
    # big_grid = build_grid(min_x, min_y, max_x, max_y, border=3)
    
    fill_grid(grid, small_points)
    # fill_grid(big_grid, big_points)

    # big_points_by_ids = { x.id : x for x in big_points }
    infinite_region_ids = get_infinite_region_ids(grid)
    #infinite_region_ids = []
    #for point in small_points:
    #    big_point = big_points_by_ids[point.id]
    #    if point.owned_count != big_point.owned_count:
    #        infinite_region_ids.append(point.id)
    #infinite_region_ids = set(infinite_region_ids)

    candidates = filter(lambda point: point.id not in infinite_region_ids, small_points)
    #grid.print_grid()
    #for point in small_points:
    #    print chr(point.id + ord('A')), point.owned_count
    print max(candidates, key=lambda x: x.owned_count).owned_count
    
if __name__ == "__main__":
    main()
