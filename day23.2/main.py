#!/usr/local/bin/python

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import List, Set, Tuple, TypeVar

import re


REGEX = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")


def manhattan_distance(left: Tuple[int, int, int], right: Tuple[int, int, int]) -> int:
    """
    Returns the 3-d Manhattan distance between [left] and [right]."""
    return abs(left[0] - right[0]) + abs(left[1] - right[1]) + abs(left[2] - right[2])


def closest_power_of_two(value: int) -> int:
    """
    The smallest power of two greater than or equal to [value]."""
    result = 1
    while result < value:
        result *= 2

    return result


@dataclass(unsafe_hash=True)
class Nanobot:
    """
    Represents a nanobot in 3 dimensions with an x,y,z position and a range."""
    position: Tuple[int, int, int]
    radius: int

    def in_range(self, other_position):
        """
        True iff the given [other_position] is in range of this Nanobot."""
        return manhattan_distance(self.position, other_position) <= self.radius


@dataclass
class OctreeNode:
    """
    A node in an Octree."""

    min_x: int
    min_y: int
    min_z: int
    left: int
    right: int
    top: int
    bottom: int
    near: int
    far: int

    def __init__(
            self,
            min_x: int,
            min_y: int,
            min_z: int,
            left: int,
            right: int,
            top: int,
            bottom: int,
            near: int,
            far: int,
            verified_nanobots: List[Nanobot],
            possible_nanobots: List[Nanobot]):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far

        self.verified_nanobots: Set[Nanobot] = set(verified_nanobots)
        for nanobot in self.verified_nanobots:
            assert is_node_fully_in_nanobot_range(
                self, nanobot), f"{self} {nanobot}"

        self.possible_nanobots: List[Nanobot] = set(filter(
            lambda nanobot: intersects(self, nanobot),
            possible_nanobots))

    @staticmethod
    def root(min_x: int, min_y: int, min_z: int, dimension: int, possible_nanobots: List[Nanobot]) -> OctreeNode:
        return OctreeNode(
            min_x=min_x,
            min_y=min_y,
            min_z=min_z,
            left=0,
            right=dimension,
            top=0,
            bottom=dimension,
            near=0,
            far=dimension,
            verified_nanobots=[],
            possible_nanobots=possible_nanobots)

    def is_single_cube(self) -> bool:
        """
        Returns true iff this node is a a single-unit cube in space, beyond which no further subdivision is possible."""
        return self.right - self.left == 1

    def closest_point_l1(self, position: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Returns the closest x,y,z point in this cell to the given position, using l1 distance."""
        if self.contains(position):
            return position

        if self.min_x + self.left <= position[0] < self.min_x + self.right:
            best_x = position[0]
        elif self.min_x + self.left <= position[0]:
            best_x = self.min_x + self.right - 1
        else:
            best_x = self.min_x + self.left

        if self.min_y + self.top <= position[1] < self.min_y + self.bottom:
            best_y = position[1]
        elif self.min_y + self.top <= position[1]:
            best_y = self.min_y + self.bottom - 1
        else:
            best_y = self.min_y + self.top

        if self.min_z + self.near <= position[2] < self.min_z + self.far:
            best_z = position[2]
        elif self.min_z + self.near <= position[2]:
            best_z = self.min_z + self.far - 1
        else:
            best_z = self.min_z + self.near

        return best_x, best_y, best_z

    def distance_to_origin(self) -> int:
        """
        The closest distance between this node and the origin."""
        origin = (0, 0, 0)
        return manhattan_distance(self.closest_point_l1(origin), origin)

    def contains(self, position: Tuple[int, int, int]):
        """
        True iff the x,y,z position given is inside this [OctreeNode]."""
        return self.min_x + self.left <= position[0] < self.min_x + self.right and \
            self.min_y + self.top <= position[1] < self.min_y + self.bottom and \
            self.min_z + self.near <= position[2] < self.min_z + self.far

    def get_corners(self) -> List[Tuple[int, int, int]]:
        """
        Returns a list with all corners of this octree. For single-cell nodes, this is single-element list.
        Otherwise, returns the 8 elements in the corners."""
        if self.is_single_cube():
            return [(self.min_x + self.left, self.min_y + self.top, self.min_z + self.near)]

        return [
            (self.min_x + self.left, self.min_y + self.top, self.min_z + self.near),
            (self.min_x + self.right - 1, self.min_y +
             self.top, self.min_z + self.near),
            (self.min_x + self.left, self.min_y +
             self.bottom - 1, self.min_z + self.near),
            (self.min_x + self.right - 1, self.min_y +
             self.bottom - 1, self.min_z + self.near),
            (self.min_x + self.left, self.min_y +
             self.top, self.min_z + self.far - 1),
            (self.min_x + self.right - 1, self.min_y +
             self.top, self.min_z + self.far - 1),
            (self.min_x + self.left, self.min_y +
             self.bottom - 1, self.min_z + self.far - 1),
            (self.min_x + self.right - 1, self.min_y +
             self.bottom - 1, self.min_z + self.far - 1),
        ]

    def subdivide(self):
        """
        Returns the subdivisions of this octree node."""
        if self.is_single_cube():
            # No further subdivision possible
            return []

        mid_x = (self.left + self.right) // 2
        mid_y = (self.top + self.bottom) // 2
        mid_z = (self.near + self.far) // 2

        return [
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=self.left, right=mid_x,
                top=self.top, bottom=mid_y,
                near=self.near, far=mid_z,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=mid_x, right=self.right,
                top=self.top, bottom=mid_y,
                near=self.near, far=mid_z,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=self.left, right=mid_x,
                top=mid_y, bottom=self.bottom,
                near=self.near, far=mid_z,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=mid_x, right=self.right,
                top=mid_y, bottom=self.bottom,
                near=self.near, far=mid_z,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=self.left, right=mid_x,
                top=self.top, bottom=mid_y,
                near=mid_z, far=self.far,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=mid_x, right=self.right,
                top=self.top, bottom=mid_y,
                near=mid_z, far=self.far,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=self.left, right=mid_x,
                top=mid_y, bottom=self.bottom,
                near=mid_z, far=self.far,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots),
            OctreeNode(
                min_x=self.min_x, min_y=self.min_y, min_z=self.min_z,
                left=mid_x, right=self.right,
                top=mid_y, bottom=self.bottom,
                near=mid_z, far=self.far,
                verified_nanobots=self.verified_nanobots,
                possible_nanobots=self.possible_nanobots)]


def is_node_fully_in_nanobot_range(node: OctreeNode, nanobot: Nanobot) -> bool:
    """
    True iff all cells in the given [node] are in range of the given [nanobot]."""
    return all(map(lambda p: nanobot.in_range(p), node.get_corners()))


def intersects(node: OctreeNode, nanobot: Nanobot) -> bool:
    """
    True iff there is a (possibly-partial) intersection between the given
    node and the range of the given nanobot."""
    return nanobot.in_range(node.closest_point_l1(nanobot.position))


def get_input() -> List[Nanobot]:
    result: List[Nanobot] = []
    try:
        while True:
            match = REGEX.match(input())
            result.append(Nanobot(
                position=(int(match.groups()[0]), int(
                    match.groups()[1]), int(match.groups()[2])),
                radius=int(match.groups()[3])))
    except EOFError:
        return result


def get_root(nanobots) -> OctreeNode:
    min_x_bot = min(nanobots, key=lambda n: n.position[0] - n.radius)
    max_x_bot = max(nanobots, key=lambda n: n.position[0] + n.radius)
    min_y_bot = min(nanobots, key=lambda n: n.position[1] - n.radius)
    max_y_bot = max(nanobots, key=lambda n: n.position[1] + n.radius)
    min_z_bot = min(nanobots, key=lambda n: n.position[2] - n.radius)
    max_z_bot = max(nanobots, key=lambda n: n.position[2] + n.radius)

    min_x = min_x_bot.position[0] - min_x_bot.radius
    max_x = max_x_bot.position[0] + max_x_bot.radius + 1
    min_y = min_y_bot.position[1] - min_y_bot.radius
    max_y = max_y_bot.position[1] + max_y_bot.radius + 1
    min_z = min_z_bot.position[2] - min_z_bot.radius
    max_z = max_z_bot.position[2] + max_z_bot.radius + 1

    dimension = max(
        closest_power_of_two(max_x - min_x),
        closest_power_of_two(max_y - min_y),
        closest_power_of_two(max_z - min_z))

    return OctreeNode.root(min_x=min_x, min_y=min_y, min_z=min_z, dimension=dimension, possible_nanobots=nanobots)


def main(interactive=False):
    nanobots = get_input()
    root = get_root(nanobots)
    print(f"Found {len(nanobots)} nanobots")

    best_node: OctreeNode = root
    queue = [best_node]
    origin: Tuple[int, int, int] = (0, 0, 0)
    while len(queue) > 0:
        # sort by distance to the origin (tie breaker)
        queue = sorted(
            queue,
            key=lambda node: manhattan_distance(node.closest_point_l1(origin), origin), reverse=True)
        # sort by number of possible hits (main criteria)
        queue = sorted(queue, key=lambda node: len(node.possible_nanobots))
        head: OctreeNode = queue.pop()

        if len(head.possible_nanobots) <= len(best_node.verified_nanobots):
            # Nothing in this node can ever beat our current best node, so it can be skipped
            # entirely
            continue

        for nanobot in head.possible_nanobots:
            if is_node_fully_in_nanobot_range(head, nanobot):
                head.verified_nanobots.add(nanobot)

            if len(head.verified_nanobots) > len(best_node.verified_nanobots):
                best_node = head

        queue += filter(
            lambda child: len(child.possible_nanobots) > len(
                best_node.verified_nanobots),
            head.subdivide())

    print(best_node)
    print(best_node.closest_point_l1(origin))
    print(len(best_node.verified_nanobots))
    print(best_node.distance_to_origin())


if __name__ == "__main__":
    main()
