from typing import List, NamedTuple, Dict, Union
from enum import IntEnum
from collections import defaultdict

Program = List[int]

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99

OPCODE_PARAMETERS = {
    OpCode.ADD: (2,1),
    OpCode.MULTIPLY: (2,1),
    OpCode.INPUT: (0,1),
    OpCode.OUTPUT: (1,0),
    OpCode.JUMP_IF_TRUE: (2,0),
    OpCode.JUMP_IF_FALSE: (2,0),
    OpCode.LESS_THAN: (2,1),
    OpCode.EQUALS: (2,1),
    OpCode.ADJUST_RELATIVE_BASE: (1,0),
    OpCode.HALT: (0,0),
}

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class Instruction(NamedTuple):
    opcode: OpCode
    inputs: List[int]
    outputs: List[int]

class Computer:
    def __init__(self, program: Program, log_output: bool=True):
        self.memory: Dict[int, int] = defaultdict(int)

        for i, value in enumerate(program):
            self.memory[i] = value

        self.log_output = log_output
        self.instruction_pointer = 0
        self.relative_base = 0
        self.halted = False
        self.waiting_for_input = False
        self.inputs: List[int] = []
        self.outputs: List[int] = []

        self.instructions = {
            OpCode.ADD: self.instruction_add,
            OpCode.MULTIPLY: self.instruction_multiply,
            OpCode.INPUT: self.instruction_input,
            OpCode.OUTPUT: self.instruction_output,
            OpCode.JUMP_IF_TRUE: self.instruction_jump_if_true,
            OpCode.JUMP_IF_FALSE: self.instruction_jump_if_false,
            OpCode.LESS_THAN: self.instruction_less_than,
            OpCode.EQUALS: self.instruction_equals,
            OpCode.ADJUST_RELATIVE_BASE: self.instruction_adjust_relative_base,
            OpCode.HALT: self.instruction_halt
        }

    def run(self, inputs: Union[List[int], str]=[]):
        if isinstance(inputs, str):
            inputs = [ord(i) for i in inputs]
        self.inputs = inputs
        self.waiting_for_input = False
        while not self.halted and not self.waiting_for_input:
            self.run_instruction()

    def run_instruction(self):
        opcode, inputs, outputs = self.read_instruction()
        self.instructions[opcode](*inputs, *outputs)

    def read(self) -> int:
        value = self.read_at(self.instruction_pointer)
        self.instruction_pointer += 1
        return value

    def read_instruction(self) -> Instruction:
        value = self.read()
        opcode = OpCode(value % 100)
        parameter_modes = value // 100

        input_parameters, output_parameters = OPCODE_PARAMETERS[opcode]

        inputs: List[int] = []
        outputs: List[int] = []

        for _ in range(input_parameters):
            parameter_mode = ParameterMode(parameter_modes % 10)
            value = self.read()

            if parameter_mode == ParameterMode.POSITION:
                value = self.read_at(value)
            elif parameter_mode == ParameterMode.RELATIVE:
                value = self.read_at(self.relative_base + value)

            inputs.append(value)

            parameter_modes //= 10

        for _ in range(output_parameters):
            parameter_mode = ParameterMode(parameter_modes % 10)
            value = self.read()

            if parameter_mode == ParameterMode.RELATIVE:
                value += self.relative_base

            outputs.append(value)

        instruction = Instruction(opcode, inputs, outputs)
        return instruction

    def read_at(self, index: int) -> int:
        assert index >= 0
        return self.memory[index]

    def write_at(self, index: int, value: int):
        assert index >= 0
        self.memory[index] = value

    def get_output(self):
        return self.outputs.pop(0)

    def get_all_output(self):
        output = self.outputs
        self.outputs = []
        return output

    def get_ascii_output(self):
        output = self.get_all_output()
        output_str = ''

        for o in output:
            if o > 128:
                output_str += str(o)
            else:
                output_str += chr(o)
        return output_str

    def instruction_add(self, input_1: int, input_2: int, output: int):
        self.write_at(output, input_1 + input_2)

    def instruction_multiply(self, input_1: int, input_2: int, output: int):
        self.write_at(output, input_1 * input_2)

    def instruction_input(self, output: int):
        if len(self.inputs) > 0:
            input = self.inputs.pop(0)
            self.write_at(output, input)
        else:
            self.waiting_for_input = True
            self.instruction_pointer -= 2

    def instruction_output(self, input: int):
        self.outputs.append(input)
        if self.log_output:
            print('Output:',input)

    def instruction_jump_if_true(self, input: int, next_instruction: int):
        if input != 0:
            self.instruction_pointer = next_instruction

    def instruction_jump_if_false(self, input: int, next_instruction: int):
        if input == 0:
            self.instruction_pointer = next_instruction

    def instruction_less_than(self, input_1: int, input_2: int, output: int):
        value = 1 if input_1 < input_2 else 0
        self.write_at(output, value)

    def instruction_equals(self, input_1: int, input_2: int, output: int):
        value = 1 if input_1 == input_2 else 0
        self.write_at(output, value)

    def instruction_adjust_relative_base(self, input: int):
        self.relative_base += input

    def instruction_halt(self):
        self.halted = True

def read_program() -> Program:
    with open('input.txt') as f:
        return [int(v) for v in f.readline().split(',')]
