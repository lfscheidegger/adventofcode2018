#!/usr/bin/python

"""
--- Part Two ---
The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which does not exist, and so the value of node C is 0.
Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2 references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0, the value of node A is 33+33+0=66.
So, in this example, the value of the root node is 66.

What is the value of the root node?
"""

from collections import defaultdict

import multiprocessing
import re
import sys


class Node:
    def __init__(self, metadata, children):
        self.metadata = metadata
        self.children = children

    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        result = 0
        for metadata_idx in self.metadata:
            if metadata_idx <= len(self.children):
                result += self.children[metadata_idx-1].value()
        return result

    def __repr__(self):
        return "Node(metadata=%s, children=%s, value=%s)" % (self.metadata, self.children, self.value())


def get_input():
    return list(int(x) for x in raw_input().strip().split())

def parse_tree(numbers):
    n_children = numbers[0]
    n_metadata = numbers[1]

    result = 0
    consumed = 2
    children = []
    for child in range(n_children):
        next_consumed, next_child = parse_tree(numbers[consumed:])
        consumed += next_consumed
        children.append(next_child)
        pass

    me = Node(children=children, metadata = numbers[consumed:consumed+n_metadata])
    return consumed + n_metadata, me


def main():
    numbers = get_input()
    print parse_tree(numbers)[1].value()
    
if __name__ == "__main__":
    main()
