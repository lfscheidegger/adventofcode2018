#!/usr/bin/python

"""
--- Day 17: Reservoir Research ---
You arrive in the year 18. If it weren't for the coat you got in 1018, you would be very cold: the North Pole base hasn't even been constructed.

Rather, it hasn't been constructed yet. The Elves are making a little progress, but there's not a lot of liquid water in this climate, so they're getting very dehydrated. Maybe there's more underground?

You scan a two-dimensional vertical slice of the ground nearby and discover that it is mostly sand with veins of clay. The scan only provides data with a granularity of square meters, but it should be good enough to determine how much water is trapped there. In the scan, x represents the distance to the right, and y represents the distance down. There is also a spring of water near the surface at x=500, y=0. The scan identifies which square meters are clay (your puzzle input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
Rendering clay as #, sand as ., and the water spring as +, and with x increasing to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...
The spring of water will produce water forever. Water can move through sand, but is blocked by clay. Water always moves down when possible, and spreads to the left and right otherwise, filling space that has clay on both sides and falling out otherwise.

For example, if five squares of water are created, they will flow downward until they reach the clay and settle there. Water that has come to rest is shown here as ~, while sand through which water has passed (but which is now dry again) is shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Two squares of water can't occupy the same location. If another five squares of water are created, they will settle on the first five, filling the clay reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Water pressure does not apply in this scenario. If another four squares of water are created, they will stay on the right side of the barrier, and no water will reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
At this point, the top reservoir overflows. While water can reach the tiles above the surface of the water, it cannot settle there, and so the next five squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...
Note especially the leftmost |: the new squares of water can reach this tile, but cannot stop there. Instead, eventually, they all fall to the right and settle in the reservoir below.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...
Finally, while there is nowhere left for the water to settle, it can reach a few more tiles before overflowing beyond the bottom of the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
How many tiles can be reached by the water? To prevent counting forever, ignore tiles with a y coordinate smaller than the smallest y coordinate in your scan data or larger than the largest one. Any x coordinate is valid. In this example, the lowest y coordinate given is 1, and the highest is 13, causing the water spring (in row 0) and the water falling off the bottom of the render (in rows 14 through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other sand tiles the water can hypothetically reach (|), the total number of tiles the water can reach is 57.

How many tiles can the water reach within the range of y values in your scan?
"""

from collections import defaultdict
from collections import deque

import multiprocessing
import re
import sys
import time

HORIZONTAL_LINE_REGEX = re.compile(r"y=(\d+), x=(\d+)\.\.(\d+)")
VERTICAL_LINE_REGEX = re.compile(r"x=(\d+), y=(\d+)\.\.(\d+)")

def get_input():
    clay_tiles = set()
    try:
        while True:
            line = raw_input()
            h_match = HORIZONTAL_LINE_REGEX.match(line)
            v_match = VERTICAL_LINE_REGEX.match(line)
            if h_match is not None:
                y = int(h_match.groups()[0])
                for x in range(int(h_match.groups()[1]), int(h_match.groups()[2]) + 1):
                    clay_tiles.add((x, y))
            elif v_match is not None:
                x = int(v_match.groups()[0])
                for y in range(int(v_match.groups()[1]), int(v_match.groups()[2]) + 1):
                    clay_tiles.add((x, y))
            else:
                raise Exception("Bad line %s" % line)
    except EOFError:
        min_x = min(clay_tiles, key=lambda t: t[0])[0] - 1
        max_x = max(clay_tiles, key=lambda t: t[0])[0] + 1

        min_y = min(clay_tiles, key=lambda t: t[1])[1] - 1
        max_y = max(clay_tiles, key=lambda t: t[1])[1] + 1

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        board = list(list('.' for x in range(width)) for y in range(height))
        for tile in clay_tiles:
            board[tile[1] - min_y][tile[0] - min_x] = '#'

        return Board(tiles=list(''.join(row) for row in board), min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)


class Board:
    def __init__(self, tiles, min_x, max_x, min_y, max_y):
        self.tiles = tiles
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        
    def __repr__(self):
        result = "\n"
        for row in self.tiles:
            result += row.replace('#', '\33[31m#\033[0m').replace('~', '\33[34m~\033[0m').replace('|', '\33[94m|\033[0m') + "\n"
        return "Board(tiles=%s, min_x=%s, max_x=%s, min_y=%s, max_y=%s)" % (result, self.min_x, self.max_x, self.min_y, self.max_y)

    def stamp(self, character, x, y):
        self.tiles[y] = self.tiles[y][:x] + character + self.tiles[y][x + 1:]

    def count_water(self):
        result = 0
        for row in self.tiles[1:-1]:
            for tile in row:
                result += 1 if tile in ['|', '~'] else 0
        return result


class FallingFront:
    """
    Represents a line of water falling vertically."""
    
    def __init__(self, x, min_y, max_y):
        self.x = x
        self.min_y = min_y
        self.max_y = max_y

    def advance(self, board):
        tiles = board.tiles
        width = len(tiles[0])
        height = len(tiles)
        while self.max_y < height - 1 and tiles[self.max_y + 1][self.x] != '#':
            self.max_y += 1
        self._stamp_on_board(board)

    def _stamp_on_board(self, board):
        for y in range(self.min_y, self.max_y + 1):
            if y < 0:
                continue
            board.stamp('|', self.x, y)


class FillingFront:
    """
    Represents a line of water spreading horizontally."""

    def __init__(self, min_x, max_x, y):
        self.min_x = min_x
        self.max_x = max_x
        self.y = y
        self.water_type = '|'

    def advance(self, board):
        tiles = board.tiles
        width = len(tiles[0])
        height = len(tiles)

        if self.y == height - 1:
            # if we're at the very bottom of the board, we can't have any clay under us by definition. So no filling,
            # just return
            return []

        # fill to the left
        while self.min_x >= 0 and tiles[self.y][self.min_x] != '#' and tiles[self.y + 1][self.min_x] in ['#', '~']:
            self.min_x -= 1
        # trim the left
        if self.min_x < 0 or tiles[self.y][self.min_x] == '#':
            self.min_x += 1
            
        # fill to the right
        while self.max_x < width and tiles[self.y][self.max_x] != '#' and tiles[self.y + 1][self.max_x] in ['#', '~']:
            self.max_x += 1
        # trim the right
        if self.max_x >= width or tiles[self.y][self.max_x] == '#':
            self.max_x -= 1

        # did we hit walls on both sides?
        if self.min_x > 0 and tiles[self.y][self.min_x - 1] == '#' and self.max_x < (width - 1) and tiles[self.y][self.max_x + 1] == '#':
            self.water_type = '~'

        self._stamp_on_board(board)

        if self.water_type == '~' or self.min_x == self.max_x:
            # if this fill stabilized, we return no new falling fronts
            return []
        else:
            result = []
            if tiles[self.y + 1][self.min_x] == '.':
                result.append(FallingFront(self.min_x, self.y + 1, self.y + 1))
            if tiles[self.y + 1][self.max_x] == '.':
                result.append(FallingFront(self.max_x, self.y + 1, self.y + 1))
            return result

    def _stamp_on_board(self, board):
        for x in range(self.min_x, self.max_x + 1):
            board.stamp(self.water_type, x, self.y)


def solve(board):
    source_position = (500 - board.min_x, -board.min_y)
    first_falling_front = FallingFront(x=source_position[0], min_y=source_position[1]+1, max_y=source_position[1]+1)

    falling_fronts = {(first_falling_front.x, first_falling_front.min_y, first_falling_front.max_y): first_falling_front}
    height = len(board.tiles)
    while len(falling_fronts) > 0:
        round_fronts = list(falling_fronts.values())
        falling_fronts.clear()
        for falling_front in round_fronts:
            falling_front.advance(board)
            y = falling_front.max_y
            if y < height - 1:
                while y >= 0:
                    filling_front = FillingFront(falling_front.x, falling_front.x, y)
                    next_falling_fronts = filling_front.advance(board)
                    if next_falling_fronts != []:
                        for next_falling_front in next_falling_fronts:
                            falling_fronts[(next_falling_front.x, next_falling_front.min_y, next_falling_front.max_y)] = next_falling_front
                        break
                    elif filling_front.water_type == '|':
                        break
                    y -= 1

    print 'Result', board.count_water()
        
def main():
    board = get_input()
    solve(board)


if __name__ == "__main__":
    main()

