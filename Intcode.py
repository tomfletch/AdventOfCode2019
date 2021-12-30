from typing import List
from enum import IntEnum

Program = List[int]

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99

class Computer:
    def __init__(self, program: Program):
        self.memory = program
        self.instruction_pointer = 0
        self.halted = False

        self.instructions = {
            OpCode.ADD: self.instruction_add,
            OpCode.MULTIPLY: self.instruction_multiply,
            OpCode.HALT: self.instruction_halt
        }

    def run(self):
        while not self.halted:
            self.run_instruction()

    def run_instruction(self):
        opcode = self.read_opcode()
        self.instructions[opcode]()

    def read(self) -> int:
        value = self.read_at(self.instruction_pointer)
        self.instruction_pointer += 1
        return value

    def read_opcode(self) -> OpCode:
        return OpCode(self.read())

    def read_at(self, index: int) -> int:
        return self.memory[index]

    def write_at(self, index: int, value: int):
        self.memory[index] = value

    def instruction_add(self):
        input_index_1 = self.read()
        input_index_2 = self.read()
        output_index = self.read()

        input_1 = self.read_at(input_index_1)
        input_2 = self.read_at(input_index_2)

        self.write_at(output_index, input_1 + input_2)

    def instruction_multiply(self):
        input_index_1 = self.read()
        input_index_2 = self.read()
        output_index = self.read()

        input_1 = self.read_at(input_index_1)
        input_2 = self.read_at(input_index_2)

        self.write_at(output_index, input_1 * input_2)

    def instruction_halt(self):
        self.halted = True

def read_program() -> Program:
    with open('input.txt') as f:
        return [int(v) for v in f.readline().split(',')]
