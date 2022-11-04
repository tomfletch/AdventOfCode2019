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

    nat_packet: Packet | None = None

    last_nat_y: int | None = None

    while True:
        is_idle = True

        for i in range(COMPUTER_COUNT):
            computer = computers[i]
            packet_queue = packet_queues[i]

            output = computer.get_all_output()

            while output:
                is_idle = False
                address = output.pop(0)
                x = output.pop(0)
                y = output.pop(0)

                # print(f'Computer {i} is sending packet ({x},{y}) to address {address}')
                packet = Packet(x, y)

                if address == 255:
                    print('Y value of packet to address 255:', y)
                    nat_packet = packet
                else:
                    packet_queues[address].append(packet)

            if not packet_queue:
                computer.run([-1])
            else:
                is_idle = False
                packet = packet_queue.pop(0)
                computer.run([packet.x, packet.y])

        if is_idle and nat_packet:
            print('Network is idle, sending NAT packet')
            packet_queues[0].append(nat_packet)

            if last_nat_y == nat_packet.y:
                print('Sent Y value twice:', nat_packet.y)
                return
            else:
                last_nat_y = nat_packet.y




if __name__ == '__main__':
    main()
