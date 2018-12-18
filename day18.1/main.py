#!/usr/bin/python

"""
--- Day 18: Settlers of The North Pole ---
On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a lumberyard (#). You take a scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely different. In exactly one minute, an open acre can fill with trees, a wooded acre can be converted to a lumberyard, or a lumberyard can be cleared to open ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded, or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent acres; the missing acres aren't counted.)

In particular:

An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning of the minute and changing to their new form by the end of that same minute. Changes that happen during the minute don't affect each other.

For example, suppose the lumber collection area is instead only 10 by 10 acres with this initial configuration:

Initial state:
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying the number of wooded acres by the number of lumberyards gives the total resource value after ten minutes: 37 * 31 = 1147.

What will the total resource value of the lumber collection area be after 10 minutes?
"""

from collections import defaultdict
from collections import deque

# 11:31 - 11:42

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

def main():
    board = get_input()
    for minute in range(10):
        board = advance(board)
    print get_result(board)

if __name__ == "__main__":
    main()

