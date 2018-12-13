#!/usr/bin/python

"""
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time


class Cart:
    def __init__(self, idx, direction, position):
        self.idx = idx
        self.direction = direction
        self.position = position
        self.next_turn = 'l'

    def _advance_next_turn(self):
        if self.next_turn == 'l':
            self.next_turn = 's'
        elif self.next_turn == 's':
            self.next_turn = 'r'
        elif self.next_turn == 'r':
            self.next_turn = 'l'
        else:
            raise Exception('Bad direction')

    def move(self, board):
        position = board[self.position[1]][self.position[0]]
        if position == '>' or position == '<':
            position = '-'
        elif position == '^' or position == 'v':
            position = '|'
    
        if position == '-':
            if self.direction == '<':
                self.position = self.position[0] - 1, self.position[1]
            elif self.direction == '>':
                self.position = self.position[0] + 1, self.position[1]
            else:
                raise Exception('Bad direction when moving %s %s %s' % (position, self.idx, self.direction))
        elif position  == '|':
            if self.direction == 'v':
                self.position = self.position[0], self.position[1] + 1
            elif self.direction == '^':
                self.position = self.position[0], self.position[1] - 1
            else:
                raise Exception('Bad direction when moving')
        elif position == '/':
            if self.direction == '^':
                self.direction = '>'
                self.position = self.position[0] + 1, self.position[1]
            elif self.direction == '<':
                self.direction = 'v'
                self.position = self.position[0], self.position[1] + 1
            elif self.direction == 'v':
                self.direction = '<'
                self.position = self.position[0] - 1, self.position[1]
            elif self.direction == '>':
                self.direction = '^'
                self.position = self.position[0], self.position[1] - 1
            else:
                raise Exception('Bad direction when turning %s %s %s' % (position, self.idx, self.direction))
        elif position == '\\':
            if self.direction == '>':
                self.direction = 'v'
                self.position = self.position[0], self.position[1] + 1
            elif self.direction == '^':
                self.direction = '<'
                self.position = self.position[0] - 1, self.position[1]
            elif self.direction == '<':
                self.direction = '^'
                self.position = self.position[0], self.position[1] - 1
            elif self.direction == 'v':
                self.direction = '>'
                self.position = self.position[0] + 1, self.position[1]
            else:
                raise Exception('Bad direction when turning %s %s %s' % (position, self.idx, self.direction))
        elif position == '+':
            if self.direction == '>':
                if self.next_turn == 'l':
                    self.direction = '^'
                    self.position = self.position[0], self.position[1] - 1
                elif self.next_turn == 'r':
                    self.direction = 'v'
                    self.position = self.position[0], self.position[1] + 1
                elif self.next_turn == 's':
                    self.position = self.position[0] + 1, self.position[1]
                else:
                    raise Exception('Bad next turn when intersecting')
            elif self.direction == '<':
                if self.next_turn == 'l':
                    self.direction = 'v'
                    self.position = self.position[0], self.position[1] + 1
                elif self.next_turn == 'r':
                    self.direction = '^'
                    self.position = self.position[0], self.position[1] - 1
                elif self.next_turn == 's':
                    self.position = self.position[0] - 1, self.position[1]
                else:
                    raise Exception('Bad next turn when intersecting')
            elif self.direction == '^':
                if self.next_turn == 'l':
                    self.direction = '<'
                    self.position = self.position[0] - 1, self.position[1]
                elif self.next_turn == 'r':
                    self.direction = '>'
                    self.position = self.position[0] + 1, self.position[1]
                elif self.next_turn == 's':
                    self.position = self.position[0], self.position[1] - 1
                else:
                    raise Exception('Bad next turn when intersecting')
            elif self.direction == 'v':
                if self.next_turn == 'l':
                    self.direction = '>'
                    self.position = self.position[0] + 1, self.position[1]
                elif self.next_turn == 'r':
                    self.direction = '<'
                    self.position = self.position[0] - 1, self.position[1]
                elif self.next_turn == 's':
                    self.position = self.position[0], self.position[1] + 1
                else:
                    raise Exception('Bad next turn when intersecting')                                
            self._advance_next_turn()
        else:
            raise Exception("Bad position")
                

    def __repr__(self):
        return 'Cart(idx=%s, position=%s, direction=%s)' % (self.idx, self.position, self.direction)
            
        

def get_input():
    result = []
    carts = []
    y = 0
    try:
        while True:
            line = raw_input()
            result.append(line)
            for x in range(len(line)):
                char = line[x]
                if char in ['>', '<', '^', 'v']:
                    carts.append(Cart(len(carts), char, (x, y)))
            y += 1

    except EOFError:
        return result, carts


def find_collision(carts):
    carts_by_position = defaultdict(list)
    for cart in carts:
        carts_by_position[cart.position].append(cart)

    
    first_collision = None
    colliding_carts = []
    for position in carts_by_position:
        if len(carts_by_position[position]) > 1:
            first_collision = position
            colliding_carts += carts_by_position[position]
    return first_collision, colliding_carts


def main():
    board, carts = get_input()
    carts = sorted(carts, key=lambda c: (c.position[1], c.position[0]))
    collision, colliding_carts = find_collision(carts)
    steps = 0
    while len(carts) > 1:
        carts = sorted(carts, key=lambda c: (c.position[1], c.position[0]))
        for cart in carts:
            cart.move(board)

            collision, colliding_carts = find_collision(carts)
            if colliding_carts != []:
                for colliding_cart in colliding_carts:
                    carts = filter(lambda c: c.idx != colliding_cart.idx, carts)

        steps += 1

    print carts[0].position

    
if __name__ == "__main__":
    main()
