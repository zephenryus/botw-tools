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
                with open(current_path + '/water_heights.csv', 'w') as height_file:
                    output.write('"x", "z", "height1", "height2", "unk0", "unk1", "unk2", "unk3", "unk4", "water type", "water type name"\n')
                    for index in range(0, 64*64):
                        height1, height2, unk0, unk1, unk2, unk3, unk4, water_type = struct.unpack('>BBBBBBBB', file.read(0x08))
                        x = index % 64
                        z = math.floor(index / 64)

                        if x == 0:
                            height_file.write('\n')
                        height_file.write('{0}, '.format(height2))
                        output.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}\n'
                                     .format(x, z, height1, height2, unk0, unk1, unk2, unk3, unk4, water_type, water_types[water_type]))


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild Water File Analyzer")
    parser.add_argument("filename", type=str, help="File to be parsed.")

    args = parser.parse_args()

    Water.analyze(args.filename)

    exit(1)


if __name__ == "__main__":
    main()