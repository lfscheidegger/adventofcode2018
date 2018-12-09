#!/usr/bin/python

"""
--- Day 8: Memory Maneuver ---
The sleigh is much easier to pull than you'd expect for something its weight. Unfortunately, neither you nor the Elves know which way the North Pole is from here.

You check your wrist device for anything that might help. It seems to have some kind of navigation system! Activating the navigation system produces more bad news: "Failed to start navigation system. Could not read software license file."

The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a data structure which, when processed, produces some kind of tree that can be used to calculate the license number.

The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes in the tree (or contains nodes that contain nodes, and so on).

Specifically, a node consists of:

A header, which is always exactly two numbers:
The quantity of child nodes.
The quantity of metadata entries.
Zero or more child nodes (as specified in the header).
One or more metadata entries (as specified in the header).
Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
C, which has 1 child node (D) and 1 metadata entry (2).
D, which has 0 child nodes and 1 metadata entry (99).
The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?
"""

from collections import defaultdict

import multiprocessing
import re
import sys

REGEX = re.compile("(\d+) players; last marble is worth (\d+) points")

class Input:
    def __init__(self, n_players, last_marble_value):
        self.n_players = n_players
        self.last_marble_value = last_marble_value

    def __repr__(self):
        return "Input(n_players=%s, last_marble_value=%s)" % (self.n_players, self.last_marble_value)


def get_inputs():
    result = []
    try:
        while True:
            match = REGEX.match(raw_input())
            result.append(Input(int(match.groups()[0]), int(match.groups()[1])))
    except EOFError:
        return result


def solve(input):
    board = [0]
    current_marble = 0
    next_marble_to_place = 1
    scores = list(0 for idx in range(input.n_players))
    current_player = -1

    while next_marble_to_place <= input.last_marble_value:
        one_to_clockwise = (board.index(current_marble) + 1) % len(board)
        if next_marble_to_place % 23 == 0:
            # Scoring pass            
            seven_to_counterclockwise = (board.index(current_marble) - 7) % len(board)
            six_to_counterclockwise = (seven_to_counterclockwise + 1) % len(board)
            
            scores[current_player] += next_marble_to_place + board[seven_to_counterclockwise]
            board = board[:seven_to_counterclockwise] + board[six_to_counterclockwise:]
            current_marble = board[seven_to_counterclockwise]
        elif one_to_clockwise == len(board) - 1:
            board.append(next_marble_to_place)
            current_marble = next_marble_to_place            
        else:
            board = board[:one_to_clockwise + 1] + [next_marble_to_place] + board[one_to_clockwise + 1:]
            current_marble = next_marble_to_place

        next_marble_to_place += 1
        current_player = (current_player + 1) % input.n_players

    print max(scores)
    
    
def main():
    inputs = get_inputs()
    for input in inputs:
        solve(input)
        # break

    
if __name__ == "__main__":
    main()
