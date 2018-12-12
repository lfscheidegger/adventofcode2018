#!/usr/bin/python

"""
--- Part Two ---
You realize that 20 generations aren't enough. After all, these plants will need to last another 1500 years to even reach your timeline, not to mention your future.

After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time

REGEX = re.compile(r"initial state: ((\.|#)+)")
LINE_REGEX = re.compile(r"((\.|#)+) => (\.|#)")


def get_input():
    result = []
    state_line = REGEX.match(raw_input()).groups()[0]
    state_line = [(idx, state_line[idx]) for idx in range(len(state_line))]
    try:
        while True:
            line = raw_input()
            if line == "":
                continue

            match = LINE_REGEX.match(line)
            result.append((match.groups()[0], match.groups()[2]))

    except EOFError:
        return state_line, result


def print_state_line(state_line):
    return ''.join(x[1] for x in state_line).strip(".")


def get_value(state_line):
    result = 0
    for item in state_line:
        if item[1] == "#":
            result += item[0]
    return result

SIZE = 50000000000

def main():
    state_line, transitions = get_input()
    patterns = { x[0]: x[1] for x in transitions }
    step = 0
    while step < SIZE:
        padded_state_line = []

        for left_idx in range(state_line[0][0] - 5, state_line[0][0]):
            padded_state_line.append((left_idx, '.'))
        padded_state_line += state_line
        for right_idx in range(state_line[-1][0] + 1, state_line[-1][0] + 6):
            padded_state_line.append((right_idx, '.'))

        next_state_line = []

        for idx in range(len(padded_state_line)):
            check = ''.join(x[1] for x in padded_state_line[idx:idx + 5])
            if len(check) != 5:
                continue
    
            if check in patterns:
                next_state_line.append((padded_state_line[idx+2][0], patterns[check]))
            else:
                next_state_line.append((padded_state_line[idx+2][0], "."))

        first_hash_idx = list(x[1] for x in next_state_line).index('#')
        last_hash_idx = len(next_state_line) - list(x[1] for x in next_state_line)[::-1].index('#')

        state_line_str = print_state_line(state_line)
        next_state_line_str = print_state_line(next_state_line)
        if state_line_str == next_state_line_str:
            delta = get_value(next_state_line) - get_value(state_line)
            steps_remaining = SIZE - step
            current = get_value(state_line)
            print current + delta * steps_remaining

        state_line = next_state_line[first_hash_idx:last_hash_idx]

    print step, get_value(state_line), len(state_line), state_line

    
if __name__ == "__main__":
    main()
