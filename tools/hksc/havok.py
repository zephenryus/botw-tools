import argparse
import os
import struct
from typing import BinaryIO


class Havok:
    file: BinaryIO

    def __init__(self, path):
        print("Parsing Havok file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        with open(path, 'rb') as self.file:
            section_start = 0
            self.file.seek(section_start)
            self.file.seek(0xe4, 1)
            data_0_offset, data_1_offset, data_2_offset, data_3_offset, size = struct.unpack('>5I',
                                                                                             self.file.read(0x14))
            offset = section_start + data_0_offset

            self.file.seek(offset + data_1_offset)
            data1 = []
            while self.file.tell() < offset + data_2_offset:
                data1.append(int(struct.unpack('>I', self.file.read(0x04))[0]))

            self.file.seek(offset + data_2_offset)
            data2 = []
            while self.file.tell() + 12 < offset + data_3_offset:
                data2.append({
                    "val1": int(struct.unpack('>I', self.file.read(0x04))[0]),
                    "val2": int(struct.unpack('>I', self.file.read(0x04))[0]),
                    "val3": int(struct.unpack('>I', self.file.read(0x04))[0])
                })

            self.file.seek(offset + data_3_offset)
            data3 = []
            while self.file.tell() + 12 < offset + size:
                data3.append({
                    "val1": int(struct.unpack('>I', self.file.read(0x04))[0]),
                    "val2": int(struct.unpack('>I', self.file.read(0x04))[0]),
                    "val3": int(struct.unpack('>I', self.file.read(0x04))[0])
                })

            with open('outfile.txt', 'w') as outfile:
                for index in range(len(data1)):
                    self.file.seek(offset + data1[index])
                    outfile.write("{0}\t{1}\t{2}\n".format(self.file.tell(), hex(self.file.tell()), self.file.read(0x04)))


def read_string(file):
    string = []

    while True:
        character = file.read(0x01)
        if character == b'\x00':
            return b''.join(string)
        string.append(character)


def main():
    parser = argparse.ArgumentParser(
        description='The Legend of Zelda: Breath of the Wild Havok Static Compound Parser')
    # parser.add_argument("filename", type=str, help="File to be parsed.")
    args = parser.parse_args()

    filename = "C:\\botw-data\\decompressed\\content\\NavMesh\\MainField\\20-16.hknm2"

    Havok(filename)


if __name__ == "__main__":
    main()
