import sys

import binascii

import zlib


def main(argv):
    strings = [
        b'param_root',
        b'TableNum',
        b'RepeatNumMin',
        b'RepeatNumMax',
        b'ApproachType',
        b'OccurrenceSpeedType',
        b'ColumnNum'
    ]

    for string in strings:
        print("{0:#0{1}x}".format((binascii.crc32(string) & 0xffffffff), 10) + ": " + string.decode("utf-8"))
        print(hex(zlib.crc32(string)))


if __name__ == "__main__":
    main(sys.argv[1:])
