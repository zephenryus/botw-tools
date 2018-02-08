import argparse

import os
import struct

import math


class Water:
    @staticmethod
    def analyze(path):
        filename = os.path.basename(path)
        print('Analyzing {0}...'.format(filename))

        current_path = os.path.dirname(os.path.realpath(__file__))
        print(current_path + 'water.csv')

        water_types = [
            'Water',
            'HotWater',
            'Poison',
            'Lava',
            'IceWater',
            'Mud',
            'Clear01',
            'Sea'
        ]

        with open(path, 'rb') as file:
            with open(current_path + '/water.csv', 'w') as output:
                for index in range(0, 64*64):
                    height, unk0, unk1, unk2, unk3, water_type = struct.unpack('>HHBBBB', file.read(0x08))
                    x = ((index % 64) / 64) * 32 - 16
                    y = ((math.floor(index / 64)) / 64) * 32 - 16
                    output.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n'
                                 .format(x, y, height / 0xffff, unk0, unk1, unk2, unk3, water_types[water_type]))


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild Water File Analyzer")
    parser.add_argument("filename", type=str, help="File to be parsed.")

    args = parser.parse_args()

    Water.analyze(args.filename)

    exit(1)


if __name__ == "__main__":
    main()