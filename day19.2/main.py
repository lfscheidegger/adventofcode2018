#!/usr/bin/python

"""
--- Part Two ---
A new background process immediately spins up in its place. It appears identical, but on closer inspection, you notice that this time, register 0 started with the value 1.

What value is left in register 0 when this new background process halts?
"""

from collections import defaultdict
from collections import deque

import multiprocessing
import re
import sys
import time


INSTRUCTION_REGEX = re.compile(r"(....) (\d+) (\d+) (\d+)")

IP_BOUND_REGISTER = 2

class Machine:
    def __init__(self, registers, ip=0):
        assert len(registers) == 6
        self.registers = registers
        self.ip = ip

    def run(self, instructions):
        while self.ip >= 0 and self.ip < len(instructions):
            instruction, A, B, C = instructions[self.ip]
            
            old_registers = list(self.registers)
            self.registers[IP_BOUND_REGISTER] = self.ip

            if instruction == 'addr':
                self.registers[C] = self.registers[A] + self.registers[B]
            elif instruction == 'addi':
                self.registers[C] = self.registers[A] + B
            elif instruction == 'mulr':
                self.registers[C] = self.registers[A] * self.registers[B]
            elif instruction == 'muli':
                self.registers[C] = self.registers[A] * B
            elif instruction == 'banr':
                self.registers[C] = self.registers[A] & self.registers[B]
            elif instruction == 'bani':
                self.registers[C] = self.registers[A] & B
            elif instruction == 'borr':
                self.registers[C] = self.registers[A] | self.registers[B]
            elif instruction == 'bori':
                self.registers[C] = self.registers[A] | B
            elif instruction == 'setr':
                self.registers[C] = self.registers[A]
            elif instruction == 'seti':
                self.registers[C] = A
            elif instruction == 'gtir':
                self.registers[C] = 1 if A > self.registers[B] else 0
            elif instruction == 'gtri':
                self.registers[C] = 1 if self.registers[A] > B else 0
            elif instruction == 'gtrr':
                self.registers[C] = 1 if self.registers[A] > self.registers[B] else 0
            elif instruction == 'eqir':
                self.registers[C] = 1 if A == self.registers[B] else 0
            elif instruction == 'eqri':
                self.registers[C] = 1 if self.registers[A] == B else 0
            elif instruction == 'eqrr':
                self.registers[C] = 1 if self.registers[A] == self.registers[B] else 0
            else:
                raise Exception('Bad instruction %' % instruction)

            old_ip = self.ip
            self.ip = self.registers[IP_BOUND_REGISTER] + 1
            yield (instruction, A, B, C, old_registers, self.registers, old_ip, self.ip)

def main():
    instructions = [
        ("addi", 2, 16, 2),
        ("seti", 1, 0, 1),
        ("seti", 1, 3, 3),
        ("mulr", 1, 3, 5),
        ("eqrr", 5, 4, 5),
        ("addr", 5, 2, 2),
        ("addi", 2, 1, 2),
        ("addr", 1, 0, 0),
        ("addi", 3, 1, 3),
        ("gtrr", 3, 4, 5),
        ("addr", 2, 5, 2),
        ("seti", 2, 6, 2),
        ("addi", 1, 1, 1),
        ("gtrr", 1, 4, 5),
        ("addr", 5, 2, 2),
        ("seti", 1, 1, 2),
        ("mulr", 2, 2, 2),
        ("addi", 4, 2, 4),
        ("mulr", 4, 4, 4),
        ("mulr", 2, 4, 4),
        ("muli", 4, 11, 4),
        ("addi", 5, 6, 5),
        ("mulr", 5, 2, 5),
        ("addi", 5, 19, 5),
        ("addr", 4, 5, 4),
        ("addr", 2, 0, 2),
        ("seti", 0, 7, 2),
        ("setr", 2, 6, 5),
        ("mulr", 5, 2, 5),
        ("addr", 2, 5, 5),
        ("mulr", 2, 5, 5),
        ("muli", 5, 14, 5),
        ("mulr", 5, 2, 5),
        ("addr", 4, 5, 4),
        ("seti", 0, 7, 0),
        ("seti", 0, 3, 2)]

    machine = Machine([0, 0, 0, 0, 0, 0])
    machine = Machine([0, 1, 3, 987, 987, 987], ip=3)    
    machine = Machine([1, 2, 3, 987, 987, 0], ip=3)

    print get_print_registers(machine.registers, machine.ip)
    for step in machine.run(instructions):
        (instruction, A, B, C, _, _, old_ip, ip) = step

        print get_print_instruction(old_ip, instruction, A, B, C)
        raw_input()        
        print get_print_registers(machine.registers, machine.ip)


    print machine.registers[0]

def get_print_registers(r, ip):
    return 'A=%s, B=%s, C=%s, D=%s, E=%s, F=%s (ip=%s)' % (r[0], r[1], r[2], r[3], r[4], r[5], ip)

def get_print_instruction(ip, instruction, A, B, C):
    register_names = ['A', 'B', 'C', 'D', 'E', 'F']
    if instruction == 'addr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s + %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == 'C':
            return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'addi':
        return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'mulr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s * %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == 'C':
            return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'muli':
        return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'banr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s & %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == 'C':
            return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'bani':
        return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'borr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s | %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == 'C':
            return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'bori':
        return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'setr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s' % (ip, register_names[C], ip)
        else:
            return '%2d: %s <- %s' % (ip, register_names[C], register_names[A])
    elif instruction == 'seti':
        return '%2d: %s <- %s' % (ip, register_names[C], A)
    elif instruction == 'gtir':
        return '%2d: %s <- (%s > %s ? 1 : 0)' % (ip, register_names[C], A, register_names[B])
    elif instruction == 'gtri':
        return '%2d: %s <- (%s > %s ? 1 : 0)' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'gtrr':
        return '%2d: %s <- (%s > %s ? 1 : 0)' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'eqir':
        return '%2d: %s <- (%s == %s ? 1 : 0)' % (ip, register_names[C], A, register_names[B])
    elif instruction == 'eqri':
        return '%2d: %s <- (%s == %s ? 1 : 0)' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'eqrr':
        return '%2d: %s <- (%s == %s ? 1 : 0)' % (ip, register_names[C], register_names[A], register_names[B])
    else:
        raise Exception('Bad instruction %' % instruction)

if __name__ == "__main__":
    main()

