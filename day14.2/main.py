#!/usr/bin/python

"""
--- Part Two ---
As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

51589 first appears after 9 recipes.
01245 first appears after 5 recipes.
92510 first appears after 18 recipes.
59414 first appears after 2018 recipes.
How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time


INPUT_STR = '290431'
INPUT = int(INPUT_STR)

def main():
    current_recipes = '37'
    left_elf_idx = 0
    right_elf_idx = 1
    step = 0
    while True:
        added = int(current_recipes[left_elf_idx]) + int(current_recipes[right_elf_idx])
        added_str = str(added)

        current_recipes += added_str

        left_elf_idx += int(current_recipes[left_elf_idx]) + 1
        right_elf_idx += int(current_recipes[right_elf_idx]) + 1
        left_elf_idx = left_elf_idx % len(current_recipes)
        right_elf_idx = right_elf_idx % len(current_recipes)
        if current_recipes[-len(INPUT_STR)-1:-1] == INPUT_STR:
            print len(current_recipes) - len(INPUT_STR) - 1
            break
        elif current_recipes[-len(INPUT_STR):] == INPUT_STR:
            print len(current_recipes) - len(INPUT_STR)
            break
    
        if step % 100000 == 0:
            print step, len(current_recipes), added_str

        step += 1


if __name__ == "__main__":
    main()

