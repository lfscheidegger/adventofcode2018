#!/usr/bin/python

"""
--- Part Two ---
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""

from collections import defaultdict

import multiprocessing
import re
import sys

REGEX = re.compile(r"Step (.) must be finished before step (.) can begin\.")

BIAS = 60
N_WORKERS = 5

class Node:
    def __init__(self, id):
        self.id = id
        self.parents = []
        self.parents2 = []
        self.parents3 = []
        self.children = []
        self.worker = None
        self.cost = BIAS + 1 + ord(self.id) - ord('A')
        self.is_complete = False

    def __repr__(self):
        return "Node(id=%s, parents=%s, children=%s, cost=%d)" % (self.id, map(lambda x: x.id, self.parents), map(lambda x: x.id, self.children), self.cost)

    
def simulate_work(all_tasks):
    time = 0
    tasks_being_worked_on = []
    while not all(map(lambda t: t.is_complete, all_tasks)):
        open_tasks = filter(lambda t: not t.is_complete, all_tasks)
        tasks_to_work_on = filter(lambda t: len(t.parents) == 0 and t.id not in map(lambda t2: t2.id, tasks_being_worked_on), open_tasks)
        tasks_to_work_on.sort(key=lambda t: -ord(t.id))
        print 'Want to work on', tasks_to_work_on
        tasks_to_work_on = tasks_to_work_on[:N_WORKERS]
        while len(tasks_to_work_on) > 0 and len(tasks_being_worked_on) < N_WORKERS:
            t = tasks_to_work_on.pop()
            print "Starting work on task %s" % t.id
            tasks_being_worked_on.append(t)

        print tasks_being_worked_on
        cheapest_cost = min(tasks_being_worked_on, key=lambda t: t.cost).cost
        for t in tasks_being_worked_on:
            t.cost -= cheapest_cost
            t.is_complete = t.cost == 0
            if t.is_complete:
                print "Completed task %s" % t.id
                for c in t.children:
                    c.parents = filter(lambda p: p.id != t.id, c.parents)
        tasks_being_worked_on = filter(lambda t: not t.is_complete, tasks_being_worked_on)
        time += cheapest_cost

    return time

        
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
            node_by_id[child_id].parents2.append(node_by_id[parent_id])
            node_by_id[child_id].parents3.append(node_by_id[parent_id])
            node_by_id[parent_id].children.append(node_by_id[child_id])

    except EOFError:
        return node_by_id


def main():
    nodes = get_input()
    time = simulate_work(nodes.values())
    print time
    
if __name__ == "__main__":
    main()
