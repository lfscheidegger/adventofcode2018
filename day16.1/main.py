#!/usr/bin/python

"""
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time

BEFORE_REGEX = re.compile(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]")
AFTER_REGEX = re.compile(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")


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

    def count_compatible(self):
        result = 0
        instructions = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
        for instruction in instructions:
            to_call = getattr(Sample, instruction)
            after_registers = to_call(self)
            if after_registers == self.after_registers:
                result += 1

        return result

            
def get_input():
    result = []
    try:
        while True:
            before_line = raw_input()
            instruction_line = raw_input()
            after_line = raw_input()
            _ = raw_input()

            before_groups = BEFORE_REGEX.match(before_line).groups()
            after_groups = AFTER_REGEX.match(after_line).groups()

            result.append(Sample(
                [int(before_groups[0]), int(before_groups[1]), int(before_groups[2]), int(before_groups[3])],
                list(int(x) for x in instruction_line.split()),
                [int(after_groups[0]), int(after_groups[1]), int(after_groups[2]), int(after_groups[3])]))

    except EOFError:
        return result

def main():
    samples = get_input()

    print len(filter(lambda s: s.count_compatible() >= 3, samples))
    #for sample in samples:
    #    print sample.count_compatible()

if __name__ == "__main__":
    main()

