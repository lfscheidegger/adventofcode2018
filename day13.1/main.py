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
    for position in carts_by_position:
        if len(carts_by_position[position]) > 1:
            assert first_collision is None, "Already found a collision"
            first_collision = position
    return first_collision


def print_board(board, carts):
    board_without_carts = list(line.replace(">",".").replace("v", ".").replace("^",".").replace("v",".") for line in board)

    for cart in carts:
        cart_line = board_without_carts[cart.position[1]]
        board_without_carts[cart.position[1]] = cart_line[:cart.position[0]] + cart.direction + cart_line[cart.position[0]+1:]
        
    for line in board_without_carts:
        print line


def main():
    board, carts = get_input()
    carts = sorted(carts, key=lambda c: c.position)
    collision = find_collision(carts)
    steps = 0
    while collision is None:
        for cart in carts:
            cart.move(board)
            collision = find_collision(carts)
            if collision is not None:
                break

    print collision

    
if __name__ == "__main__":
    main()
