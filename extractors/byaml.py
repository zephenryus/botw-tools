import argparse
import inspect
import json
import struct
import os

import math

import binascii

import dicttoxml
import yaml
import zlib


class NodeType:
    String = 0xa0
    Array = 0xc0
    Dictionary = 0xc1
    StringTable = 0xc2
    Boolean = 0xd0
    Integer = 0xd1
    Float = 0xd2
    Int2 = 0xd3

    Values = [
        0xa0,
        0xd0,
        0xd1,
        0xd2,
        0xd3
    ]

    Reference = [
        0xc0,
        0xc1,
        0xc2
    ]


class BYML:
    node_names_table = []
    strings_table = []
    data_object = []
    hash_table = {}

    def __init__(self, path, temp_data=None):
        print("Parsing Binary YAML file...")

        filename = os.path.basename(path)
        print("Reading " + filename + "...")

        try:
            file = open(path, 'rb')
            self.data = file.read()
        except PermissionError:
            self.data = temp_data

        signature = self.data[0x00:0x02]
        version, node_names_table_offset, strings_table_offset, root_node \
            = struct.unpack('>HIII', self.data[0x02:0x10])

        # Check file signature
        if signature != b'BY':
            print('\033[31mQuitting: {0} is not a binary YAML file\033[0m'.format(filename))
            print('\033[31mExpected b\'BY\' but saw {0}\033[0m'.format(signature))
            exit(0)

        # BotW uses version 2 of BYML
        if version != 2:
            print('\033[31mQuitting: {0} is not the correct binary YAML version\033[0m'.format(filename))
            print('\033[31mExpected 2 but saw {0}\033[0m'.format(version))
            exit(0)

        self.node_names_table = self.get_node(node_names_table_offset)

        # Make sure there is a node names table
        if len(self.node_names_table) <= 0:
            print('\033[31mQuitting: {0} does not contain a node name table\033[0m'.format(filename))
            exit(0)

        self.strings_table = self.get_node(strings_table_offset)

        # Make sure there is a strings table
        if len(self.node_names_table) <= 0:
            print('\033[31mQuitting: {0} does not contain a string table\033[0m'.format(filename))
            exit(0)

        # Get hashed names
        self.get_hash_table()

        self.data_object.append(self.get_node(root_node))

    def get_node(self, pos, node_type=None):
        if node_type is None:
            node_type = struct.unpack('<B', self.data[pos:pos + 0x01])[0]

        if node_type == NodeType.StringTable:
            return self.get_string_table(pos)

        elif node_type == NodeType.Dictionary:
            return self.get_dictionary(pos)

        elif node_type == NodeType.Array:
            return self.get_array(pos)

        elif node_type == NodeType.String:
            return self.strings_table[struct.unpack('>I', self.data[pos:pos + 0x04])[0]]

        elif node_type == NodeType.Boolean:
            boolValue = struct.unpack('>I', self.data[pos:pos + 0x04])[0]
            return True if boolValue == 1 else False

        elif node_type == NodeType.Integer:
            return struct.unpack('>I', self.data[pos:pos + 0x04])[0]

        elif node_type == NodeType.Int2:
            return struct.unpack('>L', self.data[pos:pos + 0x04])[0]

        elif node_type == NodeType.Float:
            return struct.unpack('>f', self.data[pos:pos + 0x04])[0]

    def get_string_table(self, pos):
        table = []
        length = struct.unpack('>H', self.data[pos + 0x02:pos + 0x04])[0]
        next_node = pos + 0x04

        for index in range(0, length):
            string_offset = struct.unpack('>I', self.data[next_node:next_node + 0x04])[0] + pos
            table.append(self.data[string_offset:].split(b'\x00', 1)[0].decode("utf_8", 'strict'))
            next_node += 0x04
        return table

    def get_dictionary(self, pos):
        dictionary = {}

        length = struct.unpack('>H', self.data[pos + 0x02:pos + 0x04])[0]
        next_node = pos + 0x04

        for index in range(0, length):
            node_name = struct.unpack('>I', b'\x00' + self.data[next_node:next_node + 0x03])[0]
            key = self.node_names_table[node_name]
            value_type = struct.unpack('>B', self.data[next_node + 0x03:next_node + 0x04])[0]
            value = 0

            if value_type in NodeType.Values:
                value = self.get_node(next_node + 0x04, value_type)

            elif value_type in NodeType.Reference:
                offset = struct.unpack('>I', self.data[next_node + 0x04:next_node + 0x08])[0]
                value = self.get_node(offset)

            # if key == 'HashId' or key == 'SRTHash':
            if isinstance(value, int):
                value = str(value)
                if value in self.hash_table:
                    print('that value is a hash!')
                    print("matched {0} to {1}".format(value, self.hash_table[value]))
                    value = self.hash_table[value]

            dictionary[key] = value
            next_node += 0x08

        return dictionary

    def get_array(self, pos):
        array = []
        node_types = []
        if struct.unpack('>B', self.data[pos:pos + 0x01])[0] != NodeType.Array:
            return []

        length = struct.unpack('>I', b'\x00' + self.data[pos + 0x01:pos + 0x04])[0]
        next_node = pos + 0x04

        for index in range(0, length):
            node_type = struct.unpack('>B', self.data[next_node:next_node + 0x01])[0]
            node_types.append(node_type)
            next_node += 0x01

        alignment_padding = (0x04 - (pos + 0x04 + length)) % 4
        first_node = pos + 0x04 + length + alignment_padding

        next_node = first_node

        for index in range(0, length):
            if node_types[index] in NodeType.Reference:
                offset = struct.unpack('>I', self.data[next_node:next_node + 0x04])[0]
                node = self.get_node(offset)
                # print(node)
                array.append(node)
            else:
                node = self.get_node(next_node, node_types[index])
                # print(node)
                array.append(node)
            next_node += 0x04

        return array

    def get_hash_table(self):
        with open('C:\\botw-data\\src\\extractors\\hashed_names.txt', 'r', encoding='utf-8') as hash_str_file:
            data = hash_str_file.read()
            data = data.split('\n')

            for index in range(0, len(data)):
                str_hash = str(zlib.crc32(bytearray(data[index], 'utf-8')))
                self.hash_table[str_hash] = data[index]
                if data[index] == 'Item_Cook_A_01':
                    print('Item_Cook_A_01', str_hash)

        # file = open('C:\\botw-data\\src\\extractors\\hash-number-appendix.txt', 'r')
        # data = file.read()
        # data = data.split('\n')
        #
        # for index in range(0, len(data)):
        #     self.hash_table[zlib.crc32(bytearray(data[index], 'utf-8'))] = data[index]
        #
        # file.close()


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild Binary yaml file parser")
    parser.add_argument("filename", type=str, help="File to be parsed.")
    parser.add_argument("-y", "--yaml",
                        help="Exports data as a yaml file (default)",
                        action="store_true")
    parser.add_argument("-j", "--json",
                        help="Exports data as a json file",
                        action="store_true")
    parser.add_argument("-x", "--xml",
                        help="Exports data as a xml file",
                        action="store_true")
    parser.add_argument("-a", "--all",
                        help="Exports data as a yaml, json and xml file",
                        action="store_true")

    args = parser.parse_args()

    byml = BYML(args.filename)

    if args.all:
        args.yaml = True
        args.json = True
        args.xml = True

    if args.yaml:
        save_as_yaml(args, byml)

    if args.json:
        save_as_json(args, byml)

    if args.xml:
        save_as_xml(args, byml)

    if not args.yaml and not args.json and not args.xml:
        save_as_yaml(args, byml)


def save_as_yaml(args, byml):
    filename = os.path.basename(args.filename)
    print('Saving {0}.yaml...'.format(filename))
    file = open(args.filename + '.yaml', 'w')
    file.write(yaml.dump(byml.data_object))
    file.close()


def save_as_json(args, byml):
    filename = os.path.basename(args.filename)
    print('Saving {0}.json...'.format(filename))
    file = open(args.filename + '.json', 'w')
    file.write(json.dumps(byml.data_object))
    file.close()


def save_as_xml(args, byml):
    from xml.dom.minidom import parseString

    filename = os.path.basename(args.filename)
    print('Saving {0}.xml...'.format(filename))
    file = open(args.filename + '.xml', 'w')
    dom = dicttoxml.dicttoxml(byml.data_object).decode('utf-8')
    file.write(parseString(dom).toprettyxml())
    file.close()


if __name__ == "__main__":
    main()
