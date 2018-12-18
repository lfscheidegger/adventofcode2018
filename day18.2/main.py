#!/usr/bin/python

"""
--- Part Two ---
This important natural resource will need to last for at least thousands of years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?
"""

from collections import defaultdict
from collections import deque

# 11:31 - 11:42 - 11:49

import multiprocessing
import re
import sys
import time

def adjacency(position):
    return ((position[0] + x[0], position[1] + x[1]) for x in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

def get_input():
    result = []
    try:
        while True:
            result.append(raw_input())
    except EOFError:
        return result


def print_board(board):
    for row in board:
        print row
    

def advance(board):
    next_board = []
    width = len(board[0])
    height = len(board)
    for y in range(len(board)):
        row = board[y]
        next_row = []
        for x in range(len(row)):
            tile = board[y][x]
            
            neighboring_open_spaces = 0
            neighboring_lumberyards = 0
            neighboring_woods = 0
            for adj_x, adj_y in adjacency((x, y)):
                if adj_x < 0 or adj_x >= width or adj_y < 0 or adj_y >= height:
                    continue
                neighboring_open_spaces += (1 if board[adj_y][adj_x] == '.' else 0)
                neighboring_lumberyards += (1 if board[adj_y][adj_x] == '#' else 0)
                neighboring_woods += (1 if board[adj_y][adj_x] == '|' else 0)

            if tile == '.':
                if neighboring_woods >= 3:
                    next_row.append('|')
                else:
                    next_row.append('.')
            elif tile == '|':
                if neighboring_lumberyards >= 3:
                    next_row.append('#')
                else:
                    next_row.append('|')
            elif tile == '#':
                if neighboring_lumberyards >= 1 and neighboring_woods >= 1:
                    next_row.append('#')
                else:
                    next_row.append('.')
        assert len(row) == len(next_row)
        next_board.append(''.join(next_row))
    return next_board


def get_result(board):
    lumberyards = 0
    woods = 0
    for row in board:
        for tile in row:
            if tile == '#':
                lumberyards += 1
            elif tile == '|':
                woods += 1
    return lumberyards * woods

# starts at m = 625
SEQUENCE = [
    207320,
    206255,
    206340,
    202720,
    202912,
    194910,
    188280,
    179568,
    176943,
    169004,
    168336,
    164328,
    163150,
    161414,
    164268,
    165186,
    168078,
    168156,
    172920,
    174699,
    177952,
    179850,
    184800,
    187488,
    193672,
    198137,
    204125,
    203118,
    205216,
    205568,
    205056,
    203194,
    200928,
    197813,
    190774,
    180960,
    177160,
    170980,
    169106,
    166860,
    167564,
    165440,
    166599,
    169050,
    171190,
    174525,
    180900,
    183032,
    186024,
    187824,
    192766,
    195392,
    201210,
    204835,
    207192,
    206272]

def get_resources(board):
    lumberyards = 0
    woods = 0
    for row in board:
        for tile in row:
            if tile == '#':
                lumberyards += 1
            elif tile == '|':
                woods += 1
    return lumberyards * woods

def get_result(minutes):
    global SEQUENCE
    return SEQUENCE[(minutes - 625) % len(SEQUENCE)]

def main():
    # Used to find the sequence
    #board = get_input()
    #for minute in range(10000000):
    #    board = advance(board)
    #    print minute, get_resources(board)
    print get_result(1000000000 - 1)

if __name__ == "__main__":
    main()

