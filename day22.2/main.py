#!/usr/bin/python

"""
--- Part Two ---
Okay, it's time to go rescue the man's friend.

As you leave, he hands you some tools: a torch and some climbing gear. You can't equip both tools at once, but you can choose to use neither.

Tools can only be used in certain regions:

In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
You start at 0,0 (the mouth of the cave) with the torch equipped and must reach the target coordinates as quickly as possible. The regions with negative X or Y are solid rock and cannot be traversed. The fastest route might involve entering regions beyond the X or Y coordinate of the target.

You can move to an adjacent region (up, down, left, or right; never diagonally) if your currently equipped tool allows you to enter that region. Moving to an adjacent region takes one minute. (For example, if you have the torch equipped, you can move between rocky and narrow regions, but cannot enter wet regions.)

You can change your currently equipped tool or put both away if your new equipment would be valid for your current region. Switching to using the climbing gear, torch, or neither always takes seven minutes, regardless of which tools you start with. (For example, if you are in a rocky region, you can switch from the torch to the climbing gear, but you cannot switch to neither.)

Finally, once you reach the target, you need the torch equipped before you can find him in the dark. The target is always in a rocky region, so if you arrive there with climbing gear equipped, you will need to spend seven minutes switching to your torch.

For example, using the same cave system as above, starting in the top left corner (0,0) and moving to the bottom right corner (the target, 10,10) as quickly as possible, one possible route is as follows, with your current position marked X:

Initially:
X=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down:
M=.|=.|.|=.|=|=.
X|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.X=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using the torch to neither tool:
M=.|=.|.|=.|=|=.
.X=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right 3:
M=.|=.|.|=.|=|=.
.|=|X|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using neither tool to the climbing gear:
M=.|=.|.|=.|=|=.
.|=|X|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down 7:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..X==..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..=X=..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down 3:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||.X.|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||..X|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.X..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right 4:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=X||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Up 2:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===X===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using the climbing gear to the torch:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===X===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||
This is tied with other routes as the fastest way to reach the target: 45 minutes. In it, 21 minutes are spent switching tools (three times, seven minutes each) and the remaining 24 minutes are spent moving.

What is the fewest number of minutes you can take to reach the target?
"""

# 16:31 - 17:06 - 19:00

from collections import defaultdict
from collections import deque

from functools import partial
import multiprocessing
import re
import sys
import time

DEPTH = 10647
TARGET = (7, 770)

def print_cave(cave):
    global DEPTH
    for row in cave:
        print ''.join(['.', '=', '|'][idx % 3] for idx in row)


def map_cave():
    global DEPTH
    global TARGET

    # some slop for exploring
    width = 5 * TARGET[0]
    height = 5 * TARGET[1]

    erosion_levels = list(list(0 for x in range(width + 1)) for y in range(height + 1))

    for y in range(height + 1):
        geologic_index = ((y % 20183) * (48271 % 20183)) % 20183
        erosion_levels[y][0] = (geologic_index + DEPTH) % 20183    

    for x in range(width + 1):
        geologic_index = ((x % 20183) * (16807 % 20183)) % 20183
        erosion_levels[0][x] = (geologic_index + DEPTH) % 20183

    for y in range(1, height + 1):
        for x in range(1, width + 1):
            if (x, y) == TARGET:
                # TARGET erosion level is always 0
                continue
            left = erosion_levels[y][x - 1]
            top = erosion_levels[y - 1][x]
            geologic_index = ((left % 20183) * (top % 20183) % 20183)
            erosion_levels[y][x] = (geologic_index + DEPTH) % 20183

    return erosion_levels


def adjacency_hof(width, height, position):
    return filter(
        lambda pos: pos[0] >= 0 and pos[1] >= 0 and pos[0] < width and pos[1] < height,
        ((position[0] + adj[0], position[1] + adj[1]) for adj in [(1, 0), (-1, 0), (0, 1), (0, -1)]))


VALID_TOOLS = {
    '.': ['TORCH', 'CLIMBING_GEAR'],
    '=': ['CLIMBING_GEAR', 'NEITHER'],
    '|': ['TORCH', 'NEITHER'],
}


def tool_change(current_tile, next_tile, current_tool):
    if current_tile == next_tile:
        return tool_change_for_same_tile_type(current_tile, current_tool)
    else:
        return tool_change_for_different_tile_type(current_tile, next_tile, current_tool)

    
def tool_change_for_same_tile_type(tile, current_tool):
    global VALID_TOOLS
    assert current_tool in VALID_TOOLS[tile]
    if tile == '.':
        return 'TORCH' if current_tool == 'CLIMBING_GEAR' else 'CLIMBING_GEAR'
    elif tile == '=':
        return 'CLIMBING_GEAR' if current_tool == 'NEITHER' else 'NEITHER'
    elif tile == '|':
        return 'TORCH' if current_tool == 'NEITHER' else 'NEITHER'


def tool_change_for_different_tile_type(current_tile, next_tile, current_tool):
    global VALID_TOOLS
    assert current_tool in VALID_TOOLS[current_tile]
    candidates = set(VALID_TOOLS[current_tile]).intersection(set(VALID_TOOLS[next_tile]))
    assert current_tool not in candidates, '%s %s %s %s' % (current_tile, next_tile, current_tool, candidates)
    assert len(candidates) == 1
    return list(candidates)[0]

    
def can_keep_tool(current_tile, next_tile, current_tool):
    global VALID_TOOLS
    return current_tool in VALID_TOOLS[current_tile] and current_tool in VALID_TOOLS[next_tile]


def can_change_tool(current_tile, next_tile, current_tool):
    global VALID_TOOLS
    candidates = set(VALID_TOOLS[current_tile]).intersection(set(VALID_TOOLS[next_tile]))
    if len(candidates) == 1:
        return False

    return True


def find_path(cave):
    global VALID_TOOLS
    costs = { ((0, 0), 'TORCH'): 0 }
    path = {}
    width = len(cave[0])
    height = len(cave)
    
    front = [((0, 0), 'TORCH')]
    while len(front) > 0:
        front = sorted(front, key=lambda p: -costs[p])
        current_position, current_tool = front.pop()
        current_tile = ['.', '=', '|'][cave[current_position[1]][current_position[0]] % 3]
        current_cost = costs[(current_position, current_tool)]

        # Try tool changes for this tile
        for new_tool in VALID_TOOLS[current_tile]:
            if new_tool == current_tool:
                continue
            new_position = current_position
            if (new_position, new_tool) not in costs or costs[(new_position, new_tool)] > current_cost + 7:
                front.append((new_position, new_tool))
                costs[(new_position, new_tool)] = current_cost + 7 # 7 minutes to change tool
                path[(new_position, new_tool)] = (current_position, current_tool)

        # Try no tool changes for this tile
        for edge_position in adjacency_hof(width, height, current_position):
            new_position = edge_position
            next_tile = ['.', '=', '|'][cave[new_position[1]][new_position[0]] % 3]
            
            if can_keep_tool(current_tile, next_tile, current_tool):
                new_tool = current_tool
                if (new_position, new_tool) not in costs or costs[(new_position, new_tool)] > current_cost + 1:
                    front.append((new_position, new_tool))
                    costs[(new_position, new_tool)] = current_cost + 1 # just one minute
                    path[(new_position, new_tool)] = (current_position, current_tool)

    return costs, path

def print_path(path, costs, target):
    if target not in path:
        print target, costs[target]
    else:
        print_path(path, costs, path[target])
        print target, costs[target]


def main():
    global TARGET
    cave = map_cave()
    print_cave(cave)
    print
    print
    costs, path = find_path(cave)
    print 'With torch', costs[(TARGET, 'TORCH')]

if __name__ == "__main__":
    main()
