#!/usr/bin/python

"""
--- Part Two ---
A new background process immediately spins up in its place. It appears identical, but on closer inspection, you notice that this time, register 0 started with the value 1.

What value is left in register 0 when this new background process halts?
"""

# 3:26 - 3:54

from collections import defaultdict
from collections import deque

import multiprocessing
import re
import sys
import time


INSTRUCTION_REGEX = re.compile(r"(....) (\d+) (\d+) (\d+)")

IP_BOUND_REGISTER = 3

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
        ("seti", 123, 0, 4),
        ("bani", 4, 456, 4),
        ("eqri", 4, 72, 4),
        ("addr", 4, 3, 3),
        ("seti", 0, 0, 3),
        ("seti", 0, 6, 4),
        ("bori", 4, 65536, 1),
        ("seti", 678134, 1, 4),
        ("bani", 1, 255, 5),
        ("addr", 4, 5, 4),
        ("bani", 4, 16777215, 4),
        ("muli", 4, 65899, 4),
        ("bani", 4, 16777215, 4),
        ("gtir", 256, 1, 5),
        ("addr", 5, 3, 3),
        ("addi", 3, 1, 3),
        ("seti", 27, 8, 3),
        ("seti", 0, 1, 5),
        ("addi", 5, 1, 2),
        ("muli", 2, 256, 2),
        ("gtrr", 2, 1, 2),
        ("addr", 2, 3, 3),
        ("addi", 3, 1, 3),
        ("seti", 25, 7, 3),
        ("addi", 5, 1, 5),
        ("seti", 17, 1, 3),
        ("setr", 5, 3, 1),
        ("seti", 7, 8, 3),
        ("eqrr", 4, 0, 5),
        ("addr", 5, 3, 3),
        ("seti", 5, 4, 3)]

    #for instruction in instructions:
    for ip in range(len(instructions)):
        instruction = instructions[ip]
        print get_print_instruction(ip, instruction[0], instruction[1], instruction[2], instruction[3])

    machine = Machine([10961197, 0, 0, 0, 0, 0])
    #machine = Machine([0, 10961197, 0, 17, 13591713, 42817],ip=18)

    print get_print_registers(machine.registers, machine.ip)
    for step in machine.run(instructions):
        (instruction, A, B, C, _, _, old_ip, ip) = step

        if old_ip >= 28:
            print 'here'
            print get_print_instruction(old_ip, instruction, A, B, C)
            raw_input()        
            print get_print_registers(machine.registers, machine.ip)


    print machine.registers[0]

def get_print_registers(r, ip):
    return 'A=%s, B=%s, C=%s, D=%s, E=%s, F=%s (ip=%s)' % (r[0], r[1], r[2], r[3], r[4], r[5], ip)

def get_print_instruction(ip, instruction, A, B, C):
    global IP_BOUND_REGISTER
    register_names = ['A', 'B', 'C', 'D', 'E', 'F']
    if instruction == 'addr':
        if register_names[A] == 'C':
            return '%2d: %s <- %s + %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'addi':
        return '%2d: %s <- %s + %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'mulr':
        if register_names[A] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s * %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'muli':
        return '%2d: %s <- %s * %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'banr':
        if register_names[A] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s & %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'bani':
        return '%2d: %s <- %s & %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'borr':
        if register_names[A] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s | %s' % (ip, register_names[C], ip, register_names[B])
        elif register_names[B] == register_names[IP_BOUND_REGISTER]:
            return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], ip)
        else:        
            return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], register_names[B])
    elif instruction == 'bori':
        return '%2d: %s <- %s | %s' % (ip, register_names[C], register_names[A], B)
    elif instruction == 'setr':
        if register_names[A] == register_names[IP_BOUND_REGISTER]:
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

