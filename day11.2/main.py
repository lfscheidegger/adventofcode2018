#!/usr/bin/python

"""
--- Part Two ---
You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.
What is the X,Y,size identifier of the square with the largest total power?

Your puzzle input is still 8868.
"""

from collections import defaultdict

import numpy as np

import multiprocessing
import re
import sys
import time


INPUT = 8868

fuel_cells = np.zeros((300, 300))
#fuel_cells = list(list(0 for idx in range(300)) for jdx in range(300))

def fill_fuel_cells():
    global fuel_cells
    for y in range(300):
        for x in range(300):
            rack_id = x+1 + 10
            power = rack_id * (y+1) + INPUT
            power *= rack_id
            power = (power / 100) % 10
            power -= 5
            fuel_cells[x][y] = power


def get_candidates():
    result = []
    for y0 in range(300):
        for x0 in range(300):
            max_side_size = min(300 - x0, 300 - y0)
            for possible_size in range(0, max_side_size + 1):
                result.append((y0, x0, possible_size))

    return result

def process_candidate(candidate):
    x0, y0, possible_size = candidate
    return x0, y0, possible_size, np.sum(fuel_cells[x0:x0+possible_size,y0:y0+possible_size])
    
    
if __name__ == "__main__":
    fill_fuel_cells()
    candidates = get_candidates()

    p = multiprocessing.Pool(processes=8)
    results = p.map(process_candidate, candidates)

    best_power = -1
    best_x = 0
    best_y = 0
    best_size = 0
    for r in results:
        if r[3] > best_power:
            best_power = r[3]
            best_x = r[0]
            best_y = r[1]
            best_size = r[2]
            print r

    print best_x+1, best_y+1, best_size, best_power
