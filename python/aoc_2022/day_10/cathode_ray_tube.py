from aoc_2022.utils import utils


class ClockCircuit:
    pass

class Memory:

    def __init__(self, instructions) -> None:

        self.instructions = [i for i in reversed(instructions)]

    # def get_instruction(self):


class Instruction:

    def __init__(self, command, arg=None) -> None:
        self.command = command
        self.arg = arg



class CPU:

    def __init__(self, memory) -> None:
        self.memory = memory
        self.x = 1
        self.state = "idle"
        self.instruction = None
        self.cycle = 1
        self.signal_strength = {}
        self.total_signal_strength = 0


    # def addx(self, v):
    #     pass

    # def noop(self):
    #     pass

    def tick(self):

        if (self.cycle - 20) % 40 == 0:
            signal_strength = self.cycle * self.x
            print(f"cycle = {self.cycle}, X = {self.x}, signal_strength: {signal_strength}")
            self.signal_strength[self.cycle] = signal_strength
            self.total_signal_strength += signal_strength

        # if state is idle get new instruction
        if self.state == "idle":
            try:
                self.instruction = self.memory.instructions.pop()
                if self.instruction.command == "addx":
                    self.state = "addx"
            except IndexError:
                self.state = "done"
        elif self.state == "addx":
            self.x += self.instruction.arg
            self.state = "idle"

        self.cycle += 1









def solve_part_one(lines):
    instructions = []
    for line in lines:
        parts = line.split()
        command = parts[0]
        if len(parts) == 1:
            instructions.append(Instruction(command))
            continue
        arg = int(parts[1])
        instructions.append(Instruction(command, arg))

    memory = Memory(instructions)
    cpu = CPU(memory=memory)

    # ClockCircuit
    while True:
        cpu.tick()
        if cpu.state == "done":
            break

    return cpu.total_signal_strength




def solve_part_two(lines):
    pass


def main():

    args = utils.parse_args()
    lines = utils.read_puzzle_input_file(args.input_file)

    print("--- Day 10: Cathode-Ray Tube ---")
    answer_part_one = solve_part_one(lines)
    print(f"Answer part one: {answer_part_one}")

    print("--- Part Two ---")
    answer_part_two = solve_part_two(lines)
    print(f"Answer part two: {answer_part_two}")


if __name__ == "__main__":
    main()