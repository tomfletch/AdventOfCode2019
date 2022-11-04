#!/usr/bin/env python3.11
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Intcode import Computer, read_program
from typing import List, NamedTuple

class Packet(NamedTuple):
    x: int
    y: int

COMPUTER_COUNT = 50

def main():
    program = read_program()

    computers: List[Computer] = []
    packet_queues: List[List[Packet]] = []

    for i in range(COMPUTER_COUNT):
        computer = Computer(program, log_output=False)
        computers.append(computer)
        packet_queues.append([])
        computer.run([i])

    while True:
        for i in range(COMPUTER_COUNT):
            computer = computers[i]
            packet_queue = packet_queues[i]

            output = computer.get_all_output()

            while output:
                address = output.pop(0)
                x = output.pop(0)
                y = output.pop(0)

                # print(f'Computer {i} is sending packet ({x},{y}) to address {address}')

                if address == 255:
                    print('Y value of packet to address 255:', y)
                    return

                packet_queues[address].append(Packet(x, y))

            if not packet_queue:
                computer.run([-1])
            else:
                packet = packet_queue.pop(0)
                computer.run([packet.x, packet.y])



if __name__ == '__main__':
    main()
