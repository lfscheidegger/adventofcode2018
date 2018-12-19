#!/usr/bin/python

"""
--- Day 19: Go With The Flow ---
With the Elves well on their way constructing the North Pole base, you turn your attention back to understanding the inner workings of programming the device.

You can't help but notice that the device's opcodes don't contain any flow control like jump instructions. The device's manual goes on to explain:

"In programs where flow control is required, the instruction pointer can be bound to a register so that it can be manipulated directly. This way, setr/seti can function as absolute jumps, addr/addi can function as relative jumps, and other opcodes can cause truly fascinating effects."

This mechanism is achieved through a declaration like #ip 1, which would modify register 1 so that accesses to it let the program indirectly access the instruction pointer itself. To compensate for this kind of binding, there are now six registers (numbered 0 through 5); the five not bound to the instruction pointer behave as normal. Otherwise, the same rules apply as the last time you worked with this device.

When the instruction pointer is bound to a register, its value is written to that register just before each instruction is executed, and the value of that register is written back to the instruction pointer immediately after each instruction finishes execution. Afterward, move to the next instruction by adding one to the instruction pointer, even if the value in the instruction pointer was just updated by an instruction. (Because of this, instructions must effectively set the instruction pointer to the instruction before the one they want executed next.)

The instruction pointer is 0 during the first instruction, 1 during the second, and so on. If the instruction pointer ever causes the device to attempt to load an instruction outside the instructions defined in the program, the program instead immediately halts. The instruction pointer starts at 0.

It turns out that this new information is already proving useful: the CPU in the device is not very powerful, and a background process is occupying most of its time. You dump the background process' declarations and instructions to a file (your puzzle input), making sure to use the names of the opcodes rather than the numbers.

For example, suppose you have the following program:

#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
When executed, the following instructions are executed. Each line contains the value of the instruction pointer at the time the instruction started, the values of the six registers before executing the instructions (in square brackets), the instruction itself, and the values of the six registers after executing the instruction (also in square brackets).

ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1 [0, 5, 0, 0, 0, 0]
ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2 [1, 5, 6, 0, 0, 0]
ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0 [3, 5, 6, 0, 0, 0]
ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0 [5, 5, 6, 0, 0, 0]
ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5 [6, 5, 6, 0, 0, 9]
In detail, when running this program, the following events occur:

The first line (#ip 0) indicates that the instruction pointer should be bound to register 0 in this program. This is not an instruction, and so the value of the instruction pointer does not change during the processing of this line.
The instruction pointer contains 0, and so the first instruction is executed (seti 5 0 1). It updates register 0 to the current instruction pointer value (0), sets register 1 to 5, sets the instruction pointer to the value of register 0 (which has no effect, as the instruction did not modify register 0), and then adds one to the instruction pointer.
The instruction pointer contains 1, and so the second instruction, seti 6 0 2, is executed. This is very similar to the instruction before it: 6 is stored in register 2, and the instruction pointer is left with the value 2.
The instruction pointer is 2, which points at the instruction addi 0 1 0. This is like a relative jump: the value of the instruction pointer, 2, is loaded into register 0. Then, addi finds the result of adding the value in register 0 and the value 1, storing the result, 3, back in register 0. Register 0 is then copied back to the instruction pointer, which will cause it to end up 1 larger than it would have otherwise and skip the next instruction (addr 1 2 3) entirely. Finally, 1 is added to the instruction pointer.
The instruction pointer is 4, so the instruction setr 1 0 0 is run. This is like an absolute jump: it copies the value contained in register 1, 5, into register 0, which causes it to end up in the instruction pointer. The instruction pointer is then incremented, leaving it at 6.
The instruction pointer is 6, so the instruction seti 9 0 5 stores 9 into register 5. The instruction pointer is incremented, causing it to point outside the program, and so the program ends.
What value is left in register 0 when the background process halts?
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
    

def main():
    instructions, ip_bound = get_input()
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

