#!/usr/bin/python

"""
--- Part Two ---
Okay, so the facility is big.

How many rooms have a shortest path from your current location that pass through at least 1000 doors?

Your puzzle answer was 8486.
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time

def get_input():
    return raw_input().strip()[1:-1]


def find_paths_to_in_range():
    global graph

    visited = {(0, 0): 0}
    path = {}

    nodes = set(graph.keys())

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
                    
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        
        for edge in graph[min_node]:
            weight = current_weight + 1
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = [min_node]
            elif edge in visited and weight == visited[edge]:
                path[edge].append(min_node)

    return visited, path

graph = defaultdict(set)

how_far_counter = 0
how_far_result = 0
BOUNDARY = 1000
how_far_to_room = []
room_coordinates = []
def get_section_step_length_2(section, how_far_at_start=0, depth=0, coordinate_at_start=(0, 0)):
    coordinate_before_messing_up = coordinate_at_start
    global how_far_counter
    global BOUNDARY
    global graph

    parens_stack = []
    for idx in range(len(section)):
        step = section[idx]
        if step in ['E', 'N', 'W', 'S']:
            if len(parens_stack) == 0:
                old_coordinate_at_start = coordinate_at_start
                if step == 'E':
                    coordinate_at_start = (coordinate_at_start[0]+1, coordinate_at_start[1])
                elif step == 'N':
                    coordinate_at_start = (coordinate_at_start[0], coordinate_at_start[1]-1)
                elif step == 'S':
                    coordinate_at_start = (coordinate_at_start[0], coordinate_at_start[1]+1)
                elif step == 'W':
                    coordinate_at_start = (coordinate_at_start[0]-1, coordinate_at_start[1])
                room_coordinates.append((coordinate_at_start[0], coordinate_at_start[1]))
                how_far_counter += 1
                how_far_to_room.append(how_far_counter)
                graph[old_coordinate_at_start].add(coordinate_at_start)
                
        elif step == '(':
            parens_stack.append(idx)
        elif step == ')':
            starting = parens_stack.pop()
            if len(parens_stack) == 0:
                get_section_step_length_2(section[starting+1:idx], how_far_counter, depth=depth+1,coordinate_at_start=coordinate_at_start)
        elif step == '|':
            if len(parens_stack) == 0:
                how_far_counter = how_far_at_start
                coordinate_at_start = coordinate_before_messing_up
                                
def main():
    global BOUNDARY
    global how_far_to_room
    global room_coordinates
    directions = get_input()

    get_section_step_length_2(directions)
    shortest_lengths = {}
    for idx in range(len(room_coordinates)):
        coordinate = room_coordinates[idx]
        length = how_far_to_room[idx]
        if coordinate not in shortest_lengths or shortest_lengths[coordinate] > length:
            shortest_lengths[coordinate] = length

    visited, path = find_paths_to_in_range()
    print max(visited.values())
    print len(filter(lambda h: h >= 1000, visited.values()))

            
if __name__ == "__main__":
    main()
