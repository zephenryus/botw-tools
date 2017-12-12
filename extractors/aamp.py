import argparse
import codecs
import json
import struct
import xml.etree.ElementTree as ElementTree
import os

import zlib

import dicttoxml
import yaml


class NodeType:
    Node = 0x00
    Boolean = 0x00
    Float = 0x01
    Int = 0x02
    Vector2 = 0x03
    Vector3 = 0x04
    Vector4 = 0x06
    String = 0x07
    Actor = 0x08
    UnknownString = 0x0f
    UnknownUnsignedInt = 0x11
    String2 = 0x14

    Values = [
        0x00,
        0x01,
        0x02,
        0x07,
        0x08,
        0x0f,
        0x11,
        0x14
    ]

    Reference = [
    ]


class AAMP:
    data_object = {}
    hash_table = {}

    def __init__(self, path):
        print("Parsing AAMP file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        file = open(path, 'rb')
        self.data = file.read()

        signature = self.data[0x00:0x04]

        if signature != b'AAMP':
            print('\033[31mQuitting: {0} is not a AAMP file\033[0m'.format(filename))
            print('\033[31mExpected b\'AAMP\' but saw {0}\033[0m'.format(signature))
            exit(0)

        version = struct.unpack('<I', self.data[0x04:0x08])[0]
        if version != 2:
            print('\033[31mQuitting: {0} is not the correct AAMP version\033[0m'.format(filename))
            print('\033[31mExpected 2 but saw {0}\033[0m'.format(version))
            exit(0)

        # Get hashed names
        self.get_hash_table()

        root_nodes_length = struct.unpack('<I', self.data[0x18:0x1c])[0]
        pos = 0x34

        for index in range(0, root_nodes_length):
            children = {}

            node_id, unknown, offset, child_count = \
                struct.unpack('<IIHH', self.data[pos:pos + 0x0c])

            if node_id in self.hash_table:
                node_id = self.hash_table[node_id]

            node_id = str(node_id)

            self.data_object[node_id] = {}

            child_pos = offset * 4 + pos
            for child_index in range(0, child_count):
                child_node_id = struct.unpack('<I', self.data[child_pos:child_pos + 0x04])[0]
                if child_node_id in self.hash_table:
                    child_node_id = self.hash_table[child_node_id]

                child_node_id = str(child_node_id)

                children[child_node_id] = self.get_node(child_pos)
                child_pos += 0x08

            self.data_object[node_id] = children
            pos += 0x0c

    def get_hash_table(self):
        file = open('C:\\botw-data\\src\\extractors\\hashed_names.txt', 'r')
        data = file.read()
        data = data.split('\n')

        for index in range(0, len(data)):
            self.hash_table[zlib.crc32(bytearray(data[index], 'utf-8'))] = data[index]

        file = open('C:\\botw-data\\src\\extractors\\hash-number-appendix.txt', 'r')
        data = file.read()
        data = data.split('\n')

        for index in range(0, len(data)):
            self.hash_table[zlib.crc32(bytearray(data[index], 'utf-8'))] = data[index]

        file.close()

    def get_node(self, pos):
        node = {}

        node_id, offset, child_count, child_node_type \
            = struct.unpack('<IHBB', self.data[pos:pos + 0x08])

        if node_id in self.hash_table:
            node_id = self.hash_table[node_id]

        node_id = str(node_id)

        offset = offset * 4 + pos

        # print("Node id: {0}, Offset: {1}, Child Count: {2}, Child Node Type: {3}"
        #       .format(node_id, hex(offset), child_count, hex(child_node_type)))

        if child_node_type == NodeType.Node and child_count > 0:
            children = []
            for index in range(0, child_count):
                child = self.get_node(offset)
                node[child[0]] = child[1]
                offset += 0x08
            return node

        # Node = 0x00
        # Boolean = 0x00
        # Float = 0x01
        # Int = 0x02
        # Vector2 = 0x03
        # Vector3 = 0x04
        # Vector4 = 0x06
        # String = 0x07
        # Actor = 0x08
        # UnknownString = 0x0f
        # UnknownUnsignedInt = 0x11
        # String2 = 0x14

        elif child_node_type == NodeType.Boolean:
            value = struct.unpack('<I', self.data[offset:offset + 0x04])[0]
            value = True if value == 1 else False
            node[node_id] = value

        elif child_node_type == NodeType.Float:
            value = struct.unpack('<f', self.data[offset:offset + 0x04])[0]
            node[node_id] = value

        elif child_node_type == NodeType.Int:
            value = struct.unpack('<I', self.data[offset:offset + 0x04])[0]
            node[node_id] = value

        elif child_node_type == NodeType.String:
            value = self.data[offset:].decode('utf-8')
            value = value.split('\x00')
            value = value[0]
            node[node_id] = value

        elif child_node_type == NodeType.Actor:
            value = self.data[offset:].decode('utf-8')
            value = value.split('\x00')
            value = value[0]
            node[node_id] = value

        elif child_node_type == NodeType.String2:
            value = self.data[offset:].decode('utf-8')
            value = value.split('\x00')
            value = value[0]
            node[node_id] = value

        else:
            value = self.data[offset:offset + 0x04]

        return node_id, value


def main():
    parser = argparse.ArgumentParser(description="Parse the Legend of Zelda: Breath of the Wild aamp files to xml")
    parser.add_argument("filename", type=str, help="File to be parsed.")
    parser.add_argument("-x", "--xml",
                        help="Exports data as a xml file (default)",
                        action="store_true")
    parser.add_argument("-y", "--yaml",
                        help="Exports data as a yaml file",
                        action="store_true")
    parser.add_argument("-j", "--json",
                        help="Exports data as a json file",
                        action="store_true")
    parser.add_argument("-a", "--all",
                        help="Exports data as a xml, yaml and json file",
                        action="store_true")

    args = parser.parse_args()

    aamp = AAMP(args.filename)

    if args.all:
        args.yaml = True
        args.json = True
        args.xml = True

    if args.yaml:
        save_as_yaml(args, aamp)

    if args.json:
        save_as_json(args, aamp)

    if args.xml:
        save_as_xml(args, aamp)

    if not args.yaml and not args.json and not args.xml:
        save_as_xml(args, aamp)


def save_as_yaml(args, byml):
    filename = os.path.basename(args.filename)
    print('Saving {0}.yaml...'.format(filename))
    file = codecs.open(args.filename + '.yaml', 'w', 'utf-8')
    yaml.dump(byml.data_object, file, allow_unicode=True)
    file.close()


def save_as_json(args, byml):
    filename = os.path.basename(args.filename)
    print('Saving {0}.json...'.format(filename))
    file = codecs.open(args.filename + '.json', 'w', 'utf-8')
    json.dump(byml.data_object, file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    file.close()


def save_as_xml(args, byml):
    from xml.dom.minidom import parseString
    filename = os.path.basename(args.filename)
    path = os.path.dirname(os.path.abspath(args.filename))
    base_filename = os.path.splitext(filename)[0]
    print('Saving {0}...'.format(path + '\\' + base_filename + '.xml'))
    file = codecs.open(path + '\\' + base_filename + '.xml', 'w', 'utf-8')
    dom = dicttoxml.dicttoxml(byml.data_object).decode('utf-8')
    file.write(parseString(dom).toprettyxml())
    file.close()


if __name__ == "__main__":
    main()
