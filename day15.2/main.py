#!/usr/bin/python

"""
"""

from collections import defaultdict
from collections import deque

import multiprocessing
import re
import sys
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


from find_path import find_paths_to_in_range
from number import Number
from tile import Tile


TILE_SIZE_PX = 32
ELVES_POWER = 19


def adjacency(position):
    return ((x[0] + position[0], x[1] + position[1]) for x in [(0, -1), (-1, 0), (1, 0), (0, 1)])


def actor_hit_point_sort_key(actor):
    return actor.hit_points


def actor_sort_key(actor):
    return (actor.position[1], actor.position[0])

def position_sort_key(position):
    return (position[1], position[0])


class InRoundState:
    def __init__(self, state, actors):
        self.state = state
        self.actors = actors

        self._next_thing = "START_ROUND"

        self._active_actor = None
        self._active_actor_targets = []
        self._active_actor_range = []
        self._range_paths = None
        self._active_actor_selected_next_square = None
        self._victim = None
        self._rounds = 0

    def advance(self):
        # print self._next_thing
        if self._next_thing == "START_ROUND":
            self._advance_start_round()
        elif self._next_thing == "FIND_ACTIVE_ACTOR":
            self._advance_find_next_active_actor()
        elif self._next_thing == "FIND_TARGETS":
            self._advance_find_all_targets()
        elif self._next_thing == "FIND_ACTOR_RANGE":
            self._advance_find_active_actor_range()
        elif self._next_thing == "FIND_PATHS":
            self._advance_find_paths()
        elif self._next_thing == "PICK_NEXT_SQUARE":
            self._advance_pick_next_square()
        elif self._next_thing == "MOVE":
            self._advance_move()
        elif self._next_thing == "FIND_VICTIM":
            self._advance_find_victim()
        elif self._next_thing == "ATTACK":
            self._advance_attack()
        elif self._next_thing == "END_TURN":
            self._advance_end_turn()
        elif self._next_thing == "END_ROUND":
            self._advance_end_round()
        elif self._next_thing == "END_COMBAT":
            total_hit_points = sum(map(lambda a: a.hit_points, self.actors))
            print "Rounds until end:", self._rounds
            print "Total hit points:", total_hit_points
            print "Outcome:", self._rounds * total_hit_points
            time.sleep(2)
            sys.exit()
                        
    def _advance_start_round(self):        
        self._turn_order = sorted(self.actors, key=actor_sort_key)
        # print 'started round'
        self._next_thing = "FIND_ACTIVE_ACTOR"
        
    def _advance_find_next_active_actor(self):
        # filter out dead people
        self._turn_order = filter(lambda a: a in self.actors, self._turn_order)
        
        if self._active_actor is None:
            self._active_actor = self._turn_order[0]
            # print 'found active actor', self._active_actor.id
            self._next_thing = "FIND_TARGETS"
        else:
            next_idx = self._turn_order.index(self._active_actor) + 1
            if next_idx < len(self._turn_order):
                self._active_actor = self._turn_order[next_idx]
                # print 'found active actor', self._active_actor.id
                self._next_thing = "FIND_TARGETS"
            else:
                self._next_thing = "END_ROUND"

    def _advance_find_all_targets(self):
        target_type = 'E' if self._active_actor.type == 'G' else 'G'
        self._active_actor_targets = list(filter(lambda a: a.type == target_type, self.actors))
        if len(self._active_actor_targets) == 0:
            self._next_thing = "END_COMBAT"
        else:
            self._next_thing = "FIND_ACTOR_RANGE"

    def _advance_find_active_actor_range(self):
        active_actor_range = set()
        for target in self._active_actor_targets:
            for adj in adjacency(target.position):
                if self.state.board[adj[1]][adj[0]] != '#':
                    active_actor_range.add(adj)

        self._active_actor_range = sorted(active_actor_range, key=position_sort_key)
        # print 'found active range'
        if self._active_actor.position in self._active_actor_range:
            self._next_thing = "FIND_VICTIM"
        else:
            self._next_thing = "FIND_PATHS"

    def _advance_find_paths(self):
        self._range_paths = find_paths_to_in_range(self._active_actor.position, self.state.board, self.actors)
        self._next_thing = "PICK_NEXT_SQUARE"
        # print 'determined paths'

    def _advance_pick_next_square(self):
        def find_first_node_to_use(start, end):
            candidates = []
            front = path[end]
            while len(front) != 0:
                next_front = []
                for node in front:
                    if start in adjacency(node):
                        candidates.append(node)
                    elif node != start:
                        next_front += path[node]
                front = list(set(next_front))
            candidates = list(set(candidates))
            return sorted(candidates, key=position_sort_key)[0]

        visited, path = self._range_paths

        range_weights = map(lambda target: visited[target], filter(lambda target: target in visited, self._active_actor_range))
        if len(range_weights) == 0:
            self._next_thing = "END_TURN"
        else:        
            lowest_range_weight = min(map(lambda target: visited[target], filter(lambda target: target in visited, self._active_actor_range)))
            lowest_range = sorted(filter(lambda range: range in visited and visited[range] == lowest_range_weight, self._active_actor_range), key=position_sort_key)[0]
        
            if visited[lowest_range] == 1:
                assert lowest_range in adjacency(self._active_actor.position)
                self._active_actor_selected_next_square = lowest_range
            else:
                self._active_actor_selected_next_square = find_first_node_to_use(self._active_actor.position, lowest_range)
            self._next_thing = "MOVE"
            # print 'selected next square'

    def _advance_move(self):
        self._active_actor.position = self._active_actor_selected_next_square

        self._active_actor_targets = []
        self._active_actor_range = []
        self._range_paths = None
        self._active_actor_selected_next_square = None
        self._next_thing = "FIND_VICTIM"

    def _advance_find_victim(self):
        attack_candidates = []
        for adj in adjacency(self._active_actor.position):
            for target in filter(lambda a: a.type != self._active_actor.type, self.actors):
                if target.position == adj:
                    attack_candidates.append(target)

        if len(attack_candidates) != 0:
            attack_candidates = sorted(attack_candidates, key=actor_sort_key)
            attack_candidates = sorted(attack_candidates, key=actor_hit_point_sort_key)
            self._victim = attack_candidates[0]
            self._next_thing = "ATTACK"
        else:
            self._next_thing = "END_TURN"

    def _advance_attack(self):
        self._victim.hit_points -= self._active_actor.attack_power
        self._victim.hit_points = max(self._victim.hit_points, 0)
        if self._victim.type == 'E' and self._victim.hit_points == 0:
            # an elf is dead. No bueno.
            print 'An elf died. RIP.'
            sys.exit(0)
            
        # print 'attacked %s (%s - %s)' % (self._victim.id, self._victim.type, self._victim.hit_points)
        self._next_thing = "END_TURN"

    def _advance_end_turn(self):
        self._active_actor_targets = []
        self._active_actor_range = []
        self._range_paths = None
        self._next_thing = "FIND_ACTIVE_ACTOR"
        self._victim = None
        # print 'actor %s (%s) ended their turn' % (self._active_actor.id, self._active_actor.type)

        # filter out dead people
        self.actors = filter(lambda a: a.hit_points > 0, self.actors)        

    def _advance_end_round(self):
        self._active_actor = None
        self._active_actor_targets = []
        self._active_actor_range = []
        self._range_paths = None
        self._next_thing = "START_ROUND"
        self._rounds += 1
        # print 'ended round'
        
    def print_gl(self):
        if self._active_actor is not None:
            self._draw_square(self._active_actor.position, 0, 0.5, 0)

        for target in self._active_actor_targets:
            self._draw_square(target.position, 0.5, 0, 0)

        for in_range in self._active_actor_range:
            self._draw_square(in_range, 0, 0, 0.5)

        if self._range_paths is not None:
            visited = self._range_paths[0]
            max_weight = max(visited.values())
            for (x, y) in visited:
                weight = visited[(x, y)]
                Number.draw(weight, (x, y), self.state.height)
                intensity = weight / float(max_weight)
                self._draw_square((x, y), intensity, 0, intensity, 0.5)

        if self._active_actor_selected_next_square is not None:
            x, y = self._active_actor_selected_next_square
            self._draw_square((x, y), 0, 0.8, 0)

        if self._victim is not None:
            x, y = self._victim.position
            self._draw_square((x, y), 0.5, 0, 0.5, 0.5)

    def _draw_square(self, position, r, g, b, a=1):
        x = position[0]
        y = self.state.height - 1 - position[1]
        
        glColor4f(r, g, b, a)

        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x+1, y)
        glVertex2f(x+1, y+1)
        glVertex2f(x, y)
        glVertex2f(x+1, y+1)
        glVertex2f(x, y+1)
        glEnd()
        glColor3f(1, 1, 1)  

class State:
    """
    Represents the state of a cave at a point in time."""
    def __init__(self, round, board, actors):
        self.round = round
        self.board = board
        self.actors = actors
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.in_round_state = InRoundState(state=self, actors=actors)

    @staticmethod
    def from_stdin():
        """
        Reads a State from standard input."""
        board = []
        actors = []
        y = 0
        actor_id = 0
        try:
            while True:
                line = raw_input()
                for x in range(len(line)):
                    char = line[x]
                    if char == 'G' or char == 'E':
                        actors.append(Actor(actor_id, char, (x, y)))
                        actor_id += 1
                    
                line = line.replace('G', '.').replace('E', '.')
                board.append(line)
                y += 1
        except EOFError:
            return State(board=board, actors=actors, round=0)

    def advance(self):
        """
        Advances the state, by either selecting the next player, advancing that player's state, etc."""
        self.in_round_state.advance()

    def print_stdout(self):
        """
        Prints the board to standard out."""
        board = list(b for b in self.board)
        for actor in self.actors:
            actor_line = board[actor.position[1]]
            board[actor.position[1]] = actor_line[:actor.position[0]] + actor.type + actor_line[actor.position[0] + 1:]
        for row in board:
            print row

    def print_gl(self):
        """
        Displays the board in OpenGL."""
        self._draw_walls()
        self._draw_in_round_state()        
        self._draw_actors()


    def _draw_walls(self):
        for y in range(len(self.board)):
            row = self.board[y]
            for x in range(len(row)):
                tile = row[x]
                if tile == '#':
                    self._draw_tile((x, y), tile)

    def _draw_in_round_state(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        self.in_round_state.print_gl()
                    
    def _draw_actors(self):
        for actor in self.actors:
            x, y = actor.position
            y = self.height - y - 1
            self._draw_tile(actor.position, actor.type, actor.hit_points==0)
            normalized_hit_points = actor.hit_points / float(200)
            glColor3f(1 - normalized_hit_points, normalized_hit_points, 0)
            glBegin(GL_TRIANGLES)
            glVertex2f(x + 0.85, y + 0.05)
            glVertex2f(x + 0.9, y + 0.05)
            glVertex2f(x + 0.9, y + 0.05 + normalized_hit_points * 0.8)

            glVertex2f(x + 0.85, y + 0.05)
            glVertex2f(x + 0.9, y + 0.05 + normalized_hit_points * 0.8)
            glVertex2f(x + 0.85, y + 0.05 + normalized_hit_points * 0.8)
            
            glEnd()
            glColor3f(1, 1, 1)

    def _draw_tile(self, position, tile, dead=False):
        Tile(tile, position, self, dead).draw()

        
class Actor:
    def __init__(self, id, type, position):
        self.id = id
        self.type = type
        self.position = position
        self.hit_points = 200
        self.attack_power = 3 if type == 'G' else ELVES_POWER


def display_func():
    global state
    glClear(GL_COLOR_BUFFER_BIT)

    state.print_gl()
    glutSwapBuffers()


def keyboard_func(key, x, y):
    global state
    
    key = key.lower()
    if key == 'q':
        sys.exit(0)
    elif key == 'a':
        state.advance()

    glutPostRedisplay()

def reshape_func(width, height):
    global state

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0, state.width, 0, state.height, -1, 1)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)


now = 0
def idle_func():
    global now
    global state
    new_now = 1000 * time.time()
    if new_now - now > 1:
        # more than 60 ms. Let's advance
        state.advance()
        glutPostRedisplay()
        now = new_now

def init_gl():
    global state
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(max(512, state.width * TILE_SIZE_PX), max(512, state.height * TILE_SIZE_PX))

    glutCreateWindow('Elves v. Goblins')

    glutDisplayFunc(display_func)
    glutKeyboardFunc(keyboard_func)
    glutReshapeFunc(reshape_func)
    glutIdleFunc(idle_func)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glutMainLoop()


def main():
    global state
    state = State.from_stdin()

    init_gl()


if __name__ == "__main__":
    main()

