#!/usr/bin/python

"""
--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""

from collections import defaultdict

def manhattan_distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


def sum_distance_one(x, y, points):
    return sum(map(lambda point: manhattan_distance(point, (x, y)), points))


def print_grid(grid, min_x, max_x, min_y, max_y, limit):
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_y + 1):    
            if grid[(x, y)] < limit:
                line.append('#')
            else:
                line.append('.')
        print ''.join(line)


def solve(grid, min_x, max_x, min_y, max_y, points, limit):


    
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_y + 1):
            if x == min_x and y == min_y:
                # top left, must do full solve
                grid[(x, y)] = sum_distance_one(x, y, points)
            elif y == min_y:
                # first row, but not first column
                all_to_left = len(filter(lambda point: point[0] < x, points))
                all_to_right = len(filter(lambda point: point[0] >= x, points))
                grid[(x, y)] = grid[(x-1, y)] + all_to_left - all_to_right
            elif x == min_x:
                # first column, but not first row
                all_above = len(filter(lambda point: point[1] < y, points))
                all_below = len(filter(lambda point: point[1] >= y, points))
                grid[(x, y)] = grid[(x, y-1)] + all_above - all_below
            else:
                # neither first row nor first column
                all_to_left = len(filter(lambda point: point[0] < x, points))
                all_to_right = len(filter(lambda point: point[0] >= x, points))
                grid[(x, y)] = grid[(x-1, y)] + all_to_left - all_to_right

    return len(filter(lambda x: x < limit, grid.values()))


def build_grid(min_x, min_y, max_x, max_y, border=2):
    result = {}
    for y in range(min_y-border, max_y+border+1):
        for x in range(min_x-border, max_x+border+1):
            result[(x, y)] = 0

    return result


def get_input():
    result = []

    try:
        while True:
            x, y = list(int(x) for x in raw_input().split(", "))
            result.append((x, y))
    except EOFError:
        return result

    
def main():
    data = get_input()

    min_x = min(data, key=lambda x: x[0])[0]
    min_y = min(data, key=lambda x: x[1])[1]
    max_x = max(data, key=lambda x: x[0])[0]
    max_y = max(data, key=lambda x: x[1])[1]

    limit = 10000
    border = 2 * limit / len(data)

    grid = {}
    print solve(grid, min_x - border, max_x + border, min_y - border, max_y + border, data, limit)
    #print_grid(grid, min_x - border, max_x + border, min_y - border, max_y + border, limit)
    
if __name__ == "__main__":
    main()
