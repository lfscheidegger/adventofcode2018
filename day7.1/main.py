#!/usr/bin/python

"""
--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

from collections import defaultdict

import multiprocessing
import re
import sys

REGEX = re.compile(r"Step (.) must be finished before step (.) can begin\.")


class Node:
    def __init__(self, id):
        self.id = id
        self.parents = []
        self.children = []

    def __repr__(self):
        return "Node(id=%s, parents=%s, children=%s)" % (self.id, map(lambda x: x.id, self.parents), map(lambda x: x.id, self.children))


def get_order(nodes):
    result = []
    while len(nodes) > 0:
        candidates = filter(lambda x: len(x.parents) == 0, nodes)
        candidates.sort(key=lambda x: x.id)
        candidate = candidates[0]
        result.append(candidate)
        for candidate_child in candidate.children:
            candidate_child.parents = filter(
                lambda x: x.id != candidate.id,
                candidate_child.parents)
        nodes = filter(lambda x: x.id != candidate.id, nodes)
    return result

        
def get_input():
    node_by_id = {}
    try:
        while True:
            parent_id, child_id = REGEX.match(raw_input()).groups()
            if child_id not in node_by_id:
                child_node = Node(id=child_id)
                node_by_id[child_id] = child_node
            if parent_id not in node_by_id:
                parent_node = Node(id=parent_id)
                node_by_id[parent_id] = parent_node

            node_by_id[child_id].parents.append(node_by_id[parent_id])
            node_by_id[parent_id].children.append(node_by_id[child_id])

    except EOFError:
        return node_by_id


def main():
    nodes = get_input()
    result = map(lambda x: x.id, get_order(nodes.values()))
    print ''.join(result)
    
if __name__ == "__main__":
    main()
