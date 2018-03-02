#
# Made by NWPlayer123 and Stella/AboodXD, no rights reserved, feel free to do whatever
#

import os
import sys
import struct


def uint8(data, pos, bom):
    return struct.unpack(bom + "B", data[pos:pos + 1])[0]


def uint16(data, pos, bom):
    return struct.unpack(bom + "H", data[pos:pos + 2])[0]


def uint32(data, pos, bom):
    return struct.unpack(bom + "I", data[pos:pos + 4])[0]


def check(length, size, percent, count):
    length = float(length)
    size = float(size)

    test = round(length / size, 2)  # Percent complete as decimal
    test *= 100  # Percent

    if test % count == 0:
        if percent != test:  # New Number
            print(str(test)[:-2] + "%")
            percent = test

    return percent


def get_str(data):
    string = b''
    char = data[:1]
    i = 1

    while char != b'\x00':
        string += char
        if i == len(data): break  # Prevent it from looping forever

        char = data[i:i + 1]
        i += 1

    return (string.decode('utf-8'))


def yaz0_decompress(data):
    # Thanks to thakis for yaz0dec, which I modeled this on after
    # I cleaned it up in v0.2, what with bit-manipulation and looping
    # Thanks to Kinnay for suggestions to make this even faster
    print("Decompressing Yaz0....")

    pos = 16
    size = uint32(data, 4, ">")  # Uncompressed filesize
    out = []
    out_len = 0

    dstpos = 0
    percent = 0
    bits = 0
    code = 0

    if len(data) >= 5242880:
        count = 5  # 5MB is gonna take a while
    else:
        count = 10

    while len(out) < size:  # Read Entire File
        percent = check(out_len, size, percent, count)

        if bits == 0:
            code = uint8(data, pos, ">")
            pos += 1
            bits = 8

        if (code & 0x80) != 0:  # Copy 1 Byte
            out.append(data[pos])
            pos += 1
            out_len += 1

        else:
            rle = uint16(data, pos, ">")
            pos += 2

            dist = rle & 0xFFF
            dstpos = len(out) - (dist + 1)
            read = (rle >> 12)

            if (rle >> 12) == 0:
                read = (data[pos]) + 0x12
                pos += 1
            else:
                read += 2

            for x in range(read):
                out.append(out[dstpos + x])
                out_len += 1

        code <<= 1
        bits -= 1

    i = 0
    for byte in out:
        if type(byte) != bytes:
            out[i] = byte.to_bytes(1, "big")
        i += 1

    out = b''.join(out)

    return out


def sarc_extract(data, mode, filename):
    print("Reading SARC {0}....".format(filename))
    pos = 6

    name, ext = os.path.splitext(filename)

    if mode == 1:  # Don"t need to check again with normal SARC
        magic1 = data[0:4]

        if magic1 != b"SARC":
            print("Not a SARC Archive!")
            print("Writing Decompressed File....")

            with open(name + ".bin", "wb") as f:
                f.write(data)

            print("Done!")

    # Byte Order Mark
    order = uint16(data, pos, ">")
    pos += 6

    if order == 0xFEFF:  # Big Endian
        bom = ">"
    elif order == 0xFFFE:  # Little Endian
        bom = "<"
    else:
        print("Invalid BOM!")
        sys.exit(1)

    # Start of data section
    doff = uint32(data, pos, bom)
    pos += 8

    # ---------------------------------------------------------------

    magic2 = data[pos:pos + 4]
    pos += 6

    assert magic2 == b"SFAT"

    # Node Count
    node_count = uint16(data, pos, bom)
    pos += 6

    nodes = []

    print("Reading File Attribute Table...")

    for x in range(node_count):
        pos += 8

        # File Offset Start
        srt = uint32(data, pos, bom)
        pos += 4

        # File Offset End
        end = uint32(data, pos, bom)
        pos += 4

        nodes.append([srt, end])

    # ---------------------------------------------------------------
    magic3 = data[pos:pos + 4]
    pos += 8

    assert magic3 == b"SFNT"
    strings = []

    print("Reading file names....")
    no_names = 0

    if get_str(data[pos:]) == "":
        print("No file names found....")
        no_names = 1

        for x in range(node_count):
            strings.append("file" + str(x))

    else:
        for x in range(node_count):
            string = get_str(data[pos:])
            pos += len(string)

            while pos <= len(data) and data[pos] == 0x00:
                pos += 1  # Move to the next string

            strings.append(string)

    # ---------------------------------------------------------------
    print("Writing Files....")

    try:
        os.mkdir(name)
    except OSError:
        print("Folder already exists, continuing....")

    if no_names:
        print("No names found. Trying to guess the file names...")

    bntx_count = 0
    bnsh_count = 0
    flan_count = 0
    flyt_count = 0
    flim_count = 0
    gtx_count = 0
    sarc_count = 0
    szs_count = 0
    file_count = 0

    for x in range(node_count):
        filename = os.path.join(name, strings[x])

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        start, end = (doff + nodes[x][0]), (doff + nodes[x][1])
        filedata = data[start:end]

        if no_names:
            if filedata[0:4] == b"BNTX":
                filename = name + "/" + "bntx" + str(bntx_count) + ".bntx"
                bntx_count += 1

            elif filedata[0:4] == b"BNSH":
                filename = name + "/" + "bnsh" + str(bnsh_count) + ".bnsh"
                bnsh_count += 1

            elif filedata[0:4] == b"FLAN":
                filename = name + "/" + "bflan" + str(flan_count) + ".bflan"
                flan_count += 1

            elif filedata[0:4] == b"FLYT":
                filename = name + "/" + "bflyt" + str(flyt_count) + ".bflyt"
                flyt_count += 1

            elif filedata[-0x28:-0x24] == b"FLIM":
                filename = name + "/" + "bflim" + str(flim_count) + ".bflim"
                flim_count += 1

            elif filedata[0:4] == b"Gfx2":
                filename = name + "/" + "gtx" + str(gtx_count) + ".gtx"
                gtx_count += 1

            elif filedata[0:4] == b"SARC":
                filename = name + "/" + "sarc" + str(sarc_count) + ".sarc"
                sarc_count += 1

            elif filedata[0:4] == b"Yaz0":
                filename = name + "/" + "szs" + str(szs_count) + ".szs"
                szs_count += 1

            else:
                filename = name + "/" + "file" + str(file_count)
                file_count += 1

        print(filename)

        with open(filename, "wb") as f:
            f.write(filedata)

    print("Done!")


def main():
    print("SARCExtract by NWPlayer123 and Stella/AboodXD")
    print("Thanks to Kinnay and thakis")

    if len(sys.argv) != 2:
        print("Usage: SARCExtract archive.szs")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    magic = data[0:4]

    if magic == b"Yaz0":
        decompressed = yaz0_decompress(data)
        sarc_extract(decompressed, 1, sys.argv[1])

    elif magic == b"SARC":
        sarc_extract(data, 0, sys.argv[1])

    else:
        print("Unknown File Format: First 4 bytes of file must be Yaz0 or SARC")
        sys.exit(1)


if __name__ == "__main__":
    main()
