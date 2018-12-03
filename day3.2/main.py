#!/usr/bin/python

"""
--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""

from collections import defaultdict

import re
import sys

RECT_REGEX = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

class Rect:
    def __init__(self, id, left, top, width, height):
        self.id = id
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __repr__(self):
        return "Rect(id=%d, left=%d, top=%d, width=%d, height=%d)" % (self.id, self.left, self.top, self.width, self.height)

def get_input():
    result = []
    try:
        while True:
            id, left, top, width, height = RECT_REGEX.match(raw_input()).groups()
            result.append(Rect(int(id), int(left), int(top), int(width), int(height)))

    except EOFError:
        return result

def main():
    board = defaultdict(list)
    claims = get_input()
    for claim in claims:
        for x in range(claim.width):
            for y in range(claim.height):
                board[(claim.left + x, claim.top + y)].append(claim.id)

    result = None
    for claim in claims:
        is_clean = True
        for x in range(claim.width):
            if not is_clean:
                break
            for y in range(claim.height):
                if not is_clean:
                    break
                if len(board[(claim.left + x, claim.top + y)]) != 1:
                    is_clean = False
        if is_clean:
            result = claim
            break

    print "Result:", result.id

if __name__ == "__main__":
    main()
