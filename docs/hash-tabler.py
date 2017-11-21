import sys
import zlib


def main(argv):
    with open("strings.txt") as inputFile:
        strings = inputFile.readlines()

    with open("hash-table.csv", "w") as outputFile:
        outputFile.write("\"uint\", \"hex\", \"value\"\n")

        for string in strings:
            outputFile.write("%d, \"%s\", \"%s\"\n" % (
                zlib.crc32(bytearray(string, "utf-8")),
                "{0:#0{1}x}".format((zlib.crc32(bytearray(string, "utf-8")) & 0xffffffff), 10),
                string.rstrip()
            ))

    inputFile.close()
    outputFile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
