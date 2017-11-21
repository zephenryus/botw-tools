import struct
import sys


class HGHT():
    def __init__(self, fileContents):
        print("Extracting HGHT...")
        f = open(fileContents, 'rb')

        pos = 0

        for y in range(0, 0x100):
            for x in range(0, 0x100):
                print("(" + str(x) + "," + str(y) + "): " + str(int.from_bytes(f.read(2), 'little')))
        pass


def main():
    print("HGHTExtract by zephenryus")

    # if len(sys.argv) != 2:
    #     print("Usage: <inputFile>")
    #     sys.exit(1)

    # with open(sys.argv[1], "rb") as hghtFile:

    HGHT("C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\580000C0A0.hght\\580000C0A0.hght")

    sys.exit(1)


if __name__ == "__main__":
    main()
