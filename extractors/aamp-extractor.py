import json
import struct
import pprint
import sys
from enum import Enum
from xml.dom.minidom import parseString

import dicttoxml as dicttoxml


class UnknownNodeTypeException(Exception):
    pass


class Type(Enum):
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


class Node:
    NodeType = None
    Name = None
    NameHash = 0
    Children = []
    Value = None
    ValueOffset = None


def parseAAMP(data, offset=0x34, datatype='node'):
    assert data[0x00:0x04] == b'AAMP'
    print("Is AAMP")
    assert data[0x30:0x34] == b'xml\0'
    print("Is xml")

    print(datatype)

    if datatype == 'node':
        # unsigned short, unsigned char, unsigned char,
        # unsigned short, unsigned char, unsigned char
        next_offset1, next_length1, next_type1, \
        next_offset2, next_length2, next_type2 = \
            struct.unpack('<HBBHBB', data[offset + 4:offset + 12])

        assert next_type1 == 0
        assert next_type2 == 0

        next_offset1 = offset + 4 * next_offset1
        next_offset2 = offset + 4 * next_offset2

        parsed_list1 = []
        for i in range(next_length1):
            # parsed_list1.append(parseAAMP(data, next_offset1 + 12 * i, 'node'))
            parsed_list1.append(parseAAMP(data, next_offset1 + 12 * i, 'node'))

        parsed_list2 = []
        for i in range(next_length2):
            parsed_list2.append(parseAAMP(data, next_offset2 + 8 * i, 0))

        return {'nodeList1': parsed_list1, 'nodeList2': parsed_list2}

    # Boolean
    elif datatype == 0x0:

        next_offset, next_length, next_type = \
            struct.unpack('<HBB', data[offset + 4:offset + 8])

        next_offset = offset + 4 * next_offset

        if next_type == 0:
            parsed_list = []
            for i in range(next_length):
                parsed_list.append(parseAAMP(data, next_offset + 8 * i, next_type))
            return parsed_list
        else:
            assert next_length == 0
            return parseAAMP(data, next_offset, next_type)

    # Float
    elif datatype == 0x1:
        print("Parsing Float")
        return struct.unpack('<f', data[offset:offset + 4])[0]

    # Int
    elif datatype == 0x2:
        print("Parsing Int")
        return struct.unpack('<I', data[offset:offset + 4])[0]

    # Vector2
    elif datatype == 0x3:
        print("Parsing Vector2")
        print(data[offset:offset + 4])
        # return struct.unpack('<I', data[offset:offset + 4])[0]

    # Vector3
    elif datatype == 0x4:
        print("Parsing Vector3")
        print(data[offset:offset + 4])
        return struct.unpack('<f', data[offset:offset + 4])

    elif datatype == 0x5:
        print(data[offset:offset + 4])

    elif datatype == 0x6:
        # Vector4
        print("Parsing Vector4")
        print(data[offset:offset + 4])
        return struct.unpack('<f', data[offset:offset + 4])

    # Strings
    elif datatype in (0x7, 0xF, 0x14):
        print("Parsing String")
        try:
            str = data[offset:].split(b'\0', 1)[0].decode('ascii')
            print(str)
            return str
        except UnicodeDecodeError:
            return data[offset:].split(b'\0', 1)[0]

    elif datatype == 0x8:
        print(data[offset:offset + 4])

    elif datatype == 0x11:
        return struct.unpack('<I', data[offset:offset + 4])[0]

    else:
        raise UnknownNodeTypeException('0x%X: 0x%02X' % (offset, datatype))


if __name__ == '__main__':
    f = open(sys.argv[1], 'rb')
    data = f.read()
    f.close()
    # pprint.pprint(parseAAMP(data))
    dom = parseString(dicttoxml.dicttoxml(parseAAMP(data), attr_type=False))
    # print(dom.toprettyxml())
