#!/usr/bin/env python3

import sys


class Packet(object):
    def __init__(self, datastream):
        self._datastream = datastream
        self._ptr = 0

        self.version = self.next_int(3)
        self.typeid = self.next_int(3)

        self.subpackets = []
        self.literal = None

        if self.typeid == 4:
            payload = []
            while True:
                bits = self.next(5)
                payload.append(bits[1:])
                if bits[0] == '0':
                    break

            self.literal = int(''.join(payload), 2)
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

    def all_subpackets(self):
        subpackets = []
        for subpacket in self.subpackets:
            subpackets.append(subpacket)
            subpackets.extend(subpacket.all_subpackets())
        return subpackets

    def pprint(self, level=0):
        print(' ' * (4 * level) +
              f'Version={self.version}, Type={self.typeid}, '
              f'Literal={self.literal or "None"}')
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
                f'literal={self.literal or "None"}, '
                f'{len(self.subpackets)} subpacket(s)')


def main():
    with open(sys.argv[1]) as f:
        datastream = ''.join(f'{int(i, 16):04b}' for i in f.read().strip())

    packet = Packet(datastream)

    print(packet.version +
          sum(p.version for p in packet.all_subpackets()))


if __name__ == '__main__':
    main()
