#!/usr/bin/env python3

import math
import sys


class Packet(object):
    def __init__(self, datastream):
        self._datastream = datastream
        self._ptr = 0

        self.version = self.next_int(3)
        self.typeid = self.next_int(3)

        self.subpackets = []

        if self.typeid == 4:
            payload = []
            while True:
                bits = self.next(5)
                payload.append(bits[1:])
                if bits[0] == '0':
                    break

            self.value = int(''.join(payload), 2)
        else:
            length_type = self.next()
            if length_type == '0':
                num_bits = self.next_int(15)
                payload = self.next(num_bits)

                while payload:
                    subpacket = Packet(payload)
                    payload = subpacket.remaining()
                    self.subpackets.append(subpacket)
            else:
                num_packets = self.next_int(11)
                payload = self.remaining()
                for i in range(num_packets):
                    subpacket = Packet(payload)
                    payload = subpacket.remaining()
                    self.subpackets.append(subpacket)

                self._datastream = payload
                self._ptr = 0

            if self.typeid == 0:
                self.value = sum(self.subpacket_values())
            elif self.typeid == 1:
                self.value = math.prod(self.subpacket_values())
            elif self.typeid == 2:
                self.value = min(self.subpacket_values())
            elif self.typeid == 3:
                self.value = max(self.subpacket_values())
            elif self.typeid == 5:
                self.value = int(self.subpackets[0].value
                                 > self.subpackets[1].value)
            elif self.typeid == 6:
                self.value = int(self.subpackets[0].value
                                 < self.subpackets[1].value)
            else:
                self.value = int(self.subpackets[0].value
                                 == self.subpackets[1].value)

    def subpacket_values(self):
        return (p.value for p in self.subpackets)

    def all_subpackets(self):
        subpackets = []
        for subpacket in self.subpackets:
            subpackets.append(subpacket)
            subpackets.extend(subpacket.all_subpackets())
        return subpackets

    def pprint(self, level=0):
        print(' ' * (4 * level) +
              f'Version={self.version}, Type={self.typeid}, '
              f'Value={self.value or "None"}')
        for subpacket in self.subpackets:
            subpacket.pprint(level + 1)

    def next(self, n=1):
        data = self._datastream[self._ptr:self._ptr + n]
        self._ptr += n
        return data

    def next_int(self, n=1):
        return int(self.next(n), 2)

    def remaining(self):
        return self._datastream[self._ptr:]

    def __repr__(self):
        return (f'Packet(version={self.version}, type={self.typeid}, '
                f'value={self.value or "None"}, '
                f'{len(self.subpackets)} subpacket(s)')


def main():
    with open(sys.argv[1]) as f:
        datastream = ''.join(f'{int(i, 16):04b}' for i in f.read().strip())

    packet = Packet(datastream)

    print('Sum of packet versions:', packet.version +
          sum(p.version for p in packet.all_subpackets()))
    print('Packet value:', packet.value)


if __name__ == '__main__':
    main()
