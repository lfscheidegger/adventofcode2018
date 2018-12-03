#!/usr/bin/python

"""
--- Part Two ---
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""

from collections import defaultdict

import sys

def get_input():
    result = []
    try:
        while True:
            result.append(raw_input())
    except EOFError:
        return result

def get_length(box_ids):
    return len(box_ids[0])

def try_one_letter(box_ids, letter_idx):
    by_shortened_id = defaultdict(list)
    for box_id in box_ids:
        shortened = box_id[:letter_idx] + box_id[letter_idx + 1:]
        by_shortened_id[shortened].append(box_id)

    # Some sanity checking
    found = False
    for shortened in by_shortened_id:
        original_ids = by_shortened_id[shortened]
        if len(original_ids) > 1:
            assert not found
            found = True

    for shortened in by_shortened_id:
        original_ids = by_shortened_id[shortened]
        if len(original_ids) > 1:
            return shortened

    return None
        
def main():
    box_ids = get_input()
    box_ids_length = get_length(box_ids)

    found = False
    for letter_idx in range(box_ids_length):
        result = try_one_letter(box_ids, letter_idx)
        if result is not None:
            print "Result:", result, "(%d)" % letter_idx
            assert not found
            found = True
            # sys.exit(0)

    if not found:
        print "Whoops"

if __name__ == "__main__":
    main()
