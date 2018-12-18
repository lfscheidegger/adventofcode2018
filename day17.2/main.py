#!/usr/bin/python

"""
--- Part Two ---
After a very long time, the water spring will run dry. How much water will be retained?

In the example above, water that won't eventually drain out is shown as ~, a total of 29 tiles.

How many water tiles are left after the water spring stops producing water and all remaining water not at rest has drained?
"""

# 11:55 - 15:52 - 15:53

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

    def count_stable_water(self):
        result = 0
        for row in self.tiles[1:-1]:
            for tile in row:
                result += 1 if tile == '~' else 0
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
    print 'Stable water', board.count_stable_water()
        
def main():
    board = get_input()
    solve(board)


if __name__ == "__main__":
    main()

