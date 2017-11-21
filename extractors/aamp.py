# python
import re
import struct
import sys
import xml.etree.ElementTree as ElementTree

from enum import Enum

import binascii


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
    Names = {
        0x00: "Boolean",
        0x01: "Float",
        0x02: "Int",
        0x03: "Vector2",
        0x04: "Vector3",
        0x05: "Unknown0x05",
        0x06: "Vector4",
        0x07: "String",
        0x08: "Actor",
        0x0f: "UnknownString",
        0x11: "UnknownUnsignedInt",
        0x14: "String2",
    }

    @staticmethod
    def getBoolean(data, pos, bom="<"):
        return struct.unpack(bom + "?", data[pos:pos + 0x01])[0]

    @staticmethod
    def getFloat(data, pos, bom="<"):
        return struct.unpack(bom + "f", data[pos:pos + 0x04])[0]

    @staticmethod
    def getInt(data, pos, bom="<"):
        return struct.unpack(bom + "I", data[pos:pos + 0x04])[0]

    @staticmethod
    def getActor(data, pos):
        return data[pos:pos + 0x04]

    @staticmethod
    def getString(data, pos):
        return data[pos:pos + 0x04]


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


ADLER_MOD = 65521


def adler32(data):
    a = 1
    b = 0

    for index in range(0, len(data)):
        a = (a + data[index]) % ADLER_MOD
        b = (b + a) % ADLER_MOD

    return (b << 16) | a


def getNode(data, nodeAddress, index):
    id = uint32(data, nodeAddress + 0x00, "<")
    offset = nodeAddress + uint16(data, nodeAddress + 0x04, "<") * 4
    childCount = uint8(data, nodeAddress + 0x06, "<")
    type = uint8(data, nodeAddress + 0x07, "<")

    if childCount > 0 and type is NodeType.Node:
        print("id: ", id,
              "\naddress: ", hex(nodeAddress),
              "\nchild count: ", childCount,
              "\nchild node offset: ", hex(offset),
              "\nnode type:  Node",
              "\nnode depth: ", index,
              "\n\n")

        for nodeIndex in range(0, childCount):
            getNode(data, offset + nodeIndex * 8, index + 1)

    elif childCount is 0:
        print("id: ", id,
              "\naddress: ", hex(nodeAddress),
              "\nnode type: ", NodeType.Names[type],
              "\nnode depth: ", index)

        if type is NodeType.Boolean:
            print("Boolean: ", NodeType.getBoolean(data, nodeAddress + 0x04))
            pass
        elif type is NodeType.Float:
            print("Float: ", NodeType.getFloat(data, nodeAddress + 0x04))
            pass
        elif type is NodeType.Int:
            print("Int: ", NodeType.getInt(data, nodeAddress + 0x04))
            pass
        elif type is NodeType.Vector2:
            print("Vector2")
            pass
        elif type is NodeType.Vector3:
            print("Vector 3")
            pass
        elif type is NodeType.Unknown0x05:
            print("Unknown0x05")
            pass
        elif type is NodeType.Vector4:
            print("Vector4")
            pass
        elif type is NodeType.String:
            print("String")
            pass
        elif type is NodeType.Actor:
            print("Actor: ", NodeType.getActor(data, nodeAddress + 0x04))
            pass
        elif type is NodeType.UnknownString:
            print("UnknownString")
            pass
        elif type is NodeType.UnknownUnsignedInt:
            print("UnknownUnsignedInt")
            pass
        elif type is NodeType.String2:
            print("String2")
            pass
        else:
            print("Unknown Node Type")

        print("\n\n")


class DataTypeParser:
    @staticmethod
    def uInt8(content, offset):
        return struct.unpack("<B", content[offset:offset + 0x01])[0]

    @staticmethod
    def uInt16(content, offset):
        return struct.unpack("<H", content[offset:offset + 0x02])[0]

    @staticmethod
    def uInt32(content, offset):
        return struct.unpack("<I", content[offset:offset + 0x04])[0]

    @staticmethod
    def string(content, offset, length=1):
        string = b""

        for index in range(offset, offset + length):
            char = content[index:index + 1]

            if char == b"\x00":
                break

            string += char

        return string.decode("utf-8")

    @staticmethod
    def byteHex(byteString):
        return "0x" + "".join("{:02x}".format(c) for c in byteString)


class AAMP():
    nodeTree = {}

    def __init__(self, fileContents):
        print("Extracting AAMP...")

        self.contents = fileContents

        assert self.isAAMP(), \
            "Unknown File Format: Expected b'AAMP' but saw %r" % self.contents[0x00:0x04]

        self.version = self.getVersion()
        assert self.version is 2, \
            "AAMP version %r is not supported, must be version 2" % self.version

        self.fileSize = self.getFileSize()

        self.dataBufferSize = self.getDataBufferSize()
        self.stringBufferSize = self.getStringBufferSize()
        self.dataBuffer = self.parseDataBuffer()
        self.stringBuffer = self.parseStringBuffer()

        self.rootNodesCount = self.getRootNodesCount()
        self.rootNodesChildCount = self.getRootNodesChildCount()
        self.totalNodes = self.getTotalNodes()

        self.fileExtensionLength = self.getFileExtensionLength()
        self.fileExtension = self.getFileExtension()

        print("File size: ", self.fileSize,
              "Root Nodes Count: ", self.rootNodesCount,
              "Total Nodes: ", self.totalNodes,
              "\nData Buffer Size: ", self.dataBufferSize,
              "\nString Buffer Size: ", self.stringBufferSize)

        print(self.dataBuffer,
              "\n",
              self.stringBuffer)

        self.ptr = 0x30 + self.fileExtensionLength

        self.parseNodes()

    def isAAMP(self):
        return self.contents[0x00:0x04] == b'AAMP'

    def getVersion(self):
        return DataTypeParser.uInt32(self.contents, 0x04)

    def getFileSize(self):
        return DataTypeParser.uInt32(self.contents, 0x0c)

    def getFileExtensionLength(self):
        return DataTypeParser.uInt32(self.contents, 0x14)

    def getRootNodesCount(self):
        return DataTypeParser.uInt32(self.contents, 0x18)

    def getRootNodesChildCount(self):
        return DataTypeParser.uInt32(self.contents, 0x1c)

    def getTotalNodes(self):
        return DataTypeParser.uInt32(self.contents, 0x20) + self.rootNodesCount + self.rootNodesChildCount

    def getDataBufferSize(self):
        return DataTypeParser.uInt32(self.contents, 0x24)

    def getStringBufferSize(self):
        return DataTypeParser.uInt32(self.contents, 0x28)

    def getFileExtension(self):
        return DataTypeParser.string(self.contents, 0x30, self.fileExtensionLength)

    def parseNodes(self):
        self.parseRootNodes()
        # self.parseChildNodes()

    def parseRootNodes(self):
        assert self.rootNodesCount > 0, \
            "There are not root nodes in this file"

        for rootNodeIndex in range(0, self.rootNodesCount):
            rootNode = RootNode(self.contents, self.ptr + rootNodeIndex * 0x0c)

    def getDataBuffer(self):
        bufferStart = self.fileSize - self.stringBufferSize - self.dataBufferSize
        bufferEnd = self.fileSize - self.stringBufferSize

        return self.contents[bufferStart:bufferEnd]

    def parseDataBuffer(self):
        dataBuffer = self.getDataBuffer()
        bufferSegmentSize = 0x02

        for ptr in range(0, int(self.dataBufferSize / bufferSegmentSize)):
            print(DataTypeParser.uInt16(dataBuffer, ptr * bufferSegmentSize))

        return dataBuffer

    def getStringBuffer(self):
        bufferStart = self.fileSize - self.stringBufferSize

        return self.contents[bufferStart:]

    def parseStringBuffer(self):
        stringBuffer = self.getStringBuffer()
        strings = []
        searchToggle = True

        for index in range(0, len(stringBuffer)):
            if stringBuffer[index] == 0x00:
                searchToggle = False
                continue

            if searchToggle is True and stringBuffer[index] != 0x00:
                continue

            string = getString(stringBuffer[index:len(stringBuffer)])
            strings.append(string)
            print(string)
            searchToggle = True

        return strings


class Node:
    fileContents = b""
    contents = b""
    id = b""
    dataOffset = 0x00
    childNodeCount = 0x00
    value = None

    nodeTree = {}

    def parseChildNodes(self, fileContents, dataOffset, childNodeCount):
        if childNodeCount > 0:
            for childNodeIndex in range(0, childNodeCount):
                childNode = ChildNode(fileContents, dataOffset + childNodeIndex * 0x08)


class RootNode(Node):
    def __init__(self, fileContents, offset):
        self.fileContents = fileContents
        self.contents = fileContents[offset:offset + 0x0c]

        self.id = self.contents[0x00:0x04]
        self.unknown = self.contents[0x04:0x08]
        self.nextNodeAddress = offset + DataTypeParser.uInt16(self.contents, 0x08) * 4
        self.childNodeCount = DataTypeParser.uInt16(self.contents, 0x0a)

        print(
            "\nAddress: ", hex(offset),
            "\nID: ", DataTypeParser.byteHex(self.id),
            "\nUnknown: ", DataTypeParser.byteHex(self.unknown),
            "\nNext Node Address: ", hex(self.nextNodeAddress),
            "\nChild Node Count: ", self.childNodeCount,
            "\n"
        )

        self.parseChildNodes(self.fileContents, self.nextNodeAddress, self.childNodeCount)


class ChildNode(Node):
    def __init__(self, fileContents, offset):
        self.fileContents = fileContents
        self.contents = fileContents[offset:offset + 0x08]

        self.id = self.contents[0x00:0x04]
        self.type = DataTypeParser.uInt8(self.contents, 0x07)
        self.childNodeCount = DataTypeParser.uInt8(self.contents, 0x06)
        self.nextNodeAddress = offset + DataTypeParser.uInt16(self.contents, 0x04) * 4

        if self.childNodeCount > 0 and self.type is NodeType.Node:
            print(
                "Address: ", hex(offset),
                "\nID: ", DataTypeParser.byteHex(self.id),
                "\nType:  Node",
                "\nnextNodeAddress: ", hex(self.nextNodeAddress),
                "\nchildNodeCount: ", self.childNodeCount,
                "\n"
            )

            self.parseChildNodes(self.fileContents, self.nextNodeAddress, self.childNodeCount)

        else:
            self.getValue(offset)

    def getValue(self, offset):
        print(
            "Address: ", hex(offset),
            "\nID: ", DataTypeParser.byteHex(self.id),
            "\nType: ", NodeType.Names[self.type]
        )
        if self.type is NodeType.Boolean:
            self.value = struct.unpack("<?", self.contents[0x04:0x04 + 0x01])[0]
            print("Boolean: ", self.value)

        elif self.type is NodeType.Float:
            self.value = struct.unpack("<f", self.contents[0x04:0x04 + 0x04])[0]
            print("Float: ", self.value)

        elif self.type is NodeType.Int:
            self.value = struct.unpack("<I", self.contents[0x04:0x04 + 0x04])[0]
            print("Int: ", self.value)

        elif self.type is NodeType.Vector2:
            pass

        elif self.type is NodeType.Vector3:
            pass

        elif self.type is NodeType.Unknown0x05:
            pass

        elif self.type is NodeType.Vector4:
            pass

        elif self.type is NodeType.String:
            pass

        elif self.type is NodeType.Actor:
            self.value = NodeType.getActor(self.contents, 0x04)
            print("Actor: ", DataTypeParser.byteHex(self.value))

        elif self.type is NodeType.UnknownString:
            pass

        elif self.type is NodeType.UnknownUnsignedInt:
            pass

        elif self.type is NodeType.String2:
            self.value = struct.unpack("<I", self.contents[0x04:0x04 + 0x04])[0]
            print("String2: ", self.value)

        else:
            pass
        print("\n")


def aampExtract(fileContents):
    print("Extracting AAMP...")

    aampVersion = uint32(fileContents, 0x04, "<")

    fileSize = uint32(fileContents, 0x0c, "<")
    stringSize = len(fileContents)

    assert fileSize == stringSize, \
        "File size checksum failed, calculated %r but actually saw %r" % (fileSize, stringSize)

    fileExtensionLength = uint32(fileContents, 0x14, "<")
    fileExtension = getString(fileContents[0x30:0x30 + fileExtensionLength])

    rootNodesCount = uint32(fileContents, 0x18, "<")
    rootNodeChildCount = uint32(fileContents, 0x1c, "<")
    totalNodes = uint32(fileContents, 0x20, "<") + rootNodesCount + rootNodeChildCount
    # print("root nodes: ", rootNodesCount)
    # print("total nodes: ", totalNodes)

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

    print(stringBuffer)

    dataBuffer = fileContents[fileSize - stringBufferSize - dataBufferSize:fileSize - stringBufferSize]

    for index in range(0, int(dataBufferSize / 4)):
        print(index, uint32(dataBuffer, index * 4, "<"))

    filePosition = 0x30 + fileExtensionLength
    nodeAddress = filePosition

    nodeId = fileContents[nodeAddress:nodeAddress + 0x04]
    assert nodeId == bytes([0x6c, 0xcb, 0xf6, 0xa4]), \
        "Invalid root node identifier, expected 6C CB F6 A4 but saw %r" % nodeId

    nodeOffset = nodeAddress + (uint16(fileContents, nodeAddress + 0x08, "<") * 4)
    rootChildCount = uint16(fileContents, nodeAddress + 0x0a, "<")

    # print("node offset:", nodeOffset)
    # print("node length:", rootChildCount)
    print("Root Node:", \
          "\nid: ", nodeId, \
          "\naddress: ", hex(nodeAddress), \
          "\nchild count: ", rootChildCount, \
          "\nchild node offset: ", hex(nodeOffset), \
          "\nnode depth: ", 0, \
          "\n\n")

    nodeAddress = nodeOffset

    aampXml = ElementTree.Element("aamp", {
        "version": str(aampVersion),
        "file-size": str(fileSize),
        "data-buffer-size": str(dataBufferSize),
        "string-buffer-size": str(stringBufferSize)
    })

    # get child nodes
    for i in range(0, rootChildCount):
        print("current location: ", hex(filePosition))
        getNode(fileContents, nodeAddress, 1)

        childCount = uint8(fileContents, nodeAddress + 0x06, "<")
        nodeAddress = nodeAddress + childCount * 0x08


def main():
    print("AAMPExtract by zephenryus")

    if len(sys.argv) != 2:
        print("Usage: <inputFile>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as aampFile:
        fileContents = aampFile.read()

    magic = fileContents[0:4]

    if magic == b"AAMP":
        AAMP(fileContents)

    else:
        print("Unknown File Format: First 4 bytes of file must be AAMP")
        sys.exit(1)


if __name__ == "__main__":
    main()
