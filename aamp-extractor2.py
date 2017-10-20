# python
import re
import struct
import sys
import xml.etree.ElementTree as ElementTree

from enum import Enum


class NodeType:
    Node = 0x00
    Boolean = 0x00
    Float = 0x01
    Int = 0x02
    Vector2 = 0x03
    Vector3 = 0x04
    Unknown0x05 = 0x05
    Vector4 = 0x06
    String = 0x07
    Actor = 0x08
    UnknownString = 0x0f
    UnknownUnsignedInt = 0x11
    String2 = 0x14


def uint8(data, pos, bom):
    return struct.unpack(bom + "B", data[pos:pos + 1])[0]


def uint16(data, pos, bom):
    return struct.unpack(bom + "H", data[pos:pos + 2])[0]


def uint32(data, pos, bom):
    return struct.unpack(bom + "I", data[pos:pos + 4])[0]


def getString(data):
    string = b""
    char = data[:1]
    i = 1

    while char != b"\x00":
        string += char
        if i == len(data): break

        char = data[i:i + 1]
        i += 1

    return (string.decode("utf-8"))


def aampExtract(fileContents):
    print("Extracting AAMP...")

    assert fileContents[0x00:0x04] == b'AAMP', \
        "Unknown File Format: Expected b'AAMP' but saw %r" % fileContents[0x00:0x04]
    aampVersion = uint32(fileContents, 0x04, "<")

    assert aampVersion is 2, \
        "AAMP version %r is not supported, must be version 2" % aampVersion

    fileSize = uint32(fileContents, 0x0c, "<")
    stringSize = len(fileContents)

    assert fileSize == stringSize, \
        "File size checksum failed, calculated %r but actually saw %r" % (fileSize, stringSize)

    fileExtensionLength = uint32(fileContents, 0x14, "<")
    fileExtension = getString(fileContents[0x30:0x30 + fileExtensionLength])

    dataBufferSize = uint32(fileContents, 0x24, "<")
    stringBufferSize = uint32(fileContents, 0x28, "<")

    strings = fileContents[fileSize - stringBufferSize:fileSize]
    stringBuffer = []
    searchToggle = False

    for index in range(0, len(strings)):
        if strings[index] == 0x00:
            searchToggle = False
            continue

        if searchToggle is True and strings[index] != 0x00:
            continue

        stringBuffer.append(getString(strings[index:len(strings)]))
        searchToggle = True

    filePosition = 0x30 + fileExtensionLength

    garbage = uint32(fileContents, filePosition, "<")  # Not completely sure what this is
    nodeOffset = filePosition + (uint16(fileContents, filePosition + 0x04, "<") * 4)
    filePosition += 0x06
    rootChildCount = uint8(fileContents, filePosition, "<")
    filePosition += 0x01
    nodeType = uint8(fileContents, filePosition, "<")
    filePosition += 0x01

    print("node offset:", nodeOffset)
    print("node length:", rootChildCount)
    print("node type:", nodeType)

    filePosition = nodeOffset

    aampXml = ElementTree.Element("aamp", {
        "version": str(aampVersion),
        "file-size": str(fileSize),
        "data-buffer-size": str(dataBufferSize),
        "string-buffer-size": str(stringBufferSize)
    })
    ElementTree.dump(aampXml)

    for i in range(0, rootChildCount):
        print("current location: ", hex(filePosition))
        garbage = uint32(fileContents, filePosition, "<")  # Not completely sure what this is
        nodeOffset = nodeOffset + 0x04 + (uint16(fileContents, filePosition + 0x04, "<") * 4)
        filePosition += 0x06
        childCount = uint8(fileContents, filePosition, "<")
        filePosition += 0x01
        nodeType = uint8(fileContents, filePosition, "<")
        filePosition += 0x01

        print("address: ", hex(nodeOffset), \
              "\nchild count: ", childCount, \
              "\nnode type: ", nodeType)

        if childCount > 0 and nodeType == NodeType.Node:
            # repeat this function
            # print("node header")
            # print(struct.unpack('<HBBHBB', fileContents[nodeAddress + 4:nodeAddress + 12]))
            pass

        else:
            if nodeType == NodeType.Boolean:
                print("boolean")

            elif nodeType == NodeType.Float:
                print(struct.unpack('<f', fileContents[filePosition:filePosition + 0x04])[0])

            pass

        nodeOffset = filePosition

    pass


def main():
    print("AAMPExtract by zephenryus")

    if len(sys.argv) != 2:
        print("Usage: aamp-extractor <inputFile>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as aampFile:
        fileContents = aampFile.read()

    magic = fileContents[0:4]

    if magic == b"AAMP":
        aampExtract(fileContents)

    else:
        print("Unknown File Format: First 4 bytes of file must be AAMP")
        sys.exit(1)


if __name__ == "__main__":
    main()
