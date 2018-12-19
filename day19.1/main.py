#!/usr/bin/python

"""
"""

from collections import defaultdict
from collections import deque

import multiprocessing
import re
import sys
import time


INSTRUCTION_REGEX = re.compile(r"(....) (\d+) (\d+) (\d+)")

class Sample:
    def __init__(self, before_registers, instruction, after_registers):
        self.before_registers = before_registers
        self.opcode = instruction[0]
        self.A = instruction[1]
        self.B = instruction[2]
        self.C = instruction[3]
        self.after_registers = after_registers

    def __repr__(self):
        return "Sample(before=%s, after=%s, opcode=%s, A=%s, B=%s, C=%s)" % (self.before_registers, self.after_registers, self.opcode, self.A, self.B, self.C)


    def addr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] + self.before_registers[self.B]
        return result

    def addi(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] + self.B
        return result

    def mulr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] * self.before_registers[self.B]
        return result

    def muli(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] * self.B
        return result

    def banr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] & self.before_registers[self.B]
        return result        

    def bani(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] & self.B
        return result

    def borr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] | self.before_registers[self.B]
        return result

    def bori(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] | self.B
        return result

    def setr(self):
        result = list(self.before_registers)
        result[self.C] = result[self.A]
        return result

    def seti(self):
        result = list(self.before_registers)
        result[self.C] = self.A
        return result

    def gtir(self):
        result = list(self.before_registers)
        if self.A > self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def gtri(self):
        result = list(self.before_registers)
        if self.before_registers[self.A] > self.B:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def gtrr(self):
        result = list(self.before_registers)
        result = list(self.before_registers)
        if self.before_registers[self.A] > self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqir(self):
        result = list(self.before_registers)
        if self.A == self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqri(self):
        result = list(self.before_registers)
        if self.before_registers[self.A] == self.B:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqrr(self):
        result = list(self.before_registers)
        result = list(self.before_registers)
        if self.before_registers[self.A] == self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

def get_input():
    try:
        result = []
        line = raw_input()
        ip_bound = int(line.split()[1])
        while True:
            line = raw_input().strip()
            match = INSTRUCTION_REGEX.match(line)
            result.append((match.groups()[0], int(match.groups()[1]), int(match.groups()[2]), int(match.groups()[3])))
            
    except EOFError:
        return result, ip_bound


class Machine:
    def __init__(self, ip_bound, instructions):
        self.registers = [0, 0, 0, 0, 0, 0]
        self.sample = Sample(self.registers, [0, 0, 0, 0], [])
        self.ip = 0
        self.ip_bound = ip_bound
        self.instructions = instructions

    def step(self):
        if self.ip < 0 or self.ip >= len(self.instructions):
            raise StopIteration
        
        next_instruction = self.instructions[self.ip]
        self._execute(next_instruction)        

    def _execute(self, instruction):
        self.registers[self.ip_bound] = self.ip
        self.sample.before_registers = self.registers
        exec_callable = getattr(Sample, instruction[0])
        self.sample.A = instruction[1]
        self.sample.B = instruction[2]
        self.sample.C = instruction[3]
        
        old_registers = list(self.registers)
        old_ip = self.ip

        self.registers = exec_callable(self.sample)
        self.ip = self.registers[self.ip_bound] + 1

        # print instruction[0], self.registers
        # print "ip=%s %s %s %s %s %s %s" % (old_ip, old_registers, instruction[0], instruction[1], instruction[2], instruction[3], self.registers)
        
    

def main():
    instructions, ip_bound = get_input()
    print instructions, ip_bound
    machine = Machine(ip_bound, instructions)
    steps = 0
    try:
        while True:
            machine.step()
            steps += 1

    except StopIteration:
        print 'Result', machine.registers[0]

if __name__ == "__main__":
    main()

