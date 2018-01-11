import argparse
import json

import os
import struct

import dicttoxml
import yaml


class TSCB:
    def __init__(self, path):
        print("Parsing Binary Terrain Scene file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        file = open(path, 'rb')
        self.data = file.read()

        signature = self.data[0x00:0x04]

        if signature != b'TSCB':
            print('\033[31mQuitting: {0} is not a binary YAML file\033[0m'.format(filename))
            print('\033[31mExpected b\'BY\' but saw {0}\033[0m'.format(signature))
            exit(0)

        # version
        # scene
        # world_scale
        # material_info_array
        # fabrication_tilling
        # file_info
        # material_info
        # mat_index
        # tex_index
        # fabrication_micro
        # scene_info
        # height_scale
        # uv_scale
        # uvw_info
        # extra_info_array
        # area_array

        area_array_offset = struct.unpack('>I', self.data[0x0c:0x10])[0]
        map_scale = {'y': struct.unpack('>f', self.data[0x10:0x14])[0],
                     'x': struct.unpack('>f', self.data[0x14:0x18])[0]}
        mat_index_length, tile_array_length, unk01, unk02, world_scale, unk03, tile_array_offset \
            = struct.unpack('>IIIIfII', self.data[0x18:0x34])

        area_array_offset += 0x10
        tile_array_offset += 0x30

        material_info_array = []
        file = open('material_info_array.csv', 'w')
        file.write(
            "mat_index, unk1, unk2, unk3, unk4\n")
        pos = 0x34

        # read material_info_array
        for index in range(0, mat_index_length):
            offset = struct.unpack('>I', self.data[pos:pos + 0x04])[0] + pos
            pos += 0x04

            mat_index, attr1, attr2, attr3, attr4 \
                = struct.unpack('>Iffff', self.data[offset:offset + 0x14])

            file.write("{0}, {1}, {2}, {3}, {4}\n".format(mat_index, attr1, attr2, attr3, attr4))
        file.close()


        file = open('area_array.csv', 'w')
        file.write(
            "pos_x, pos_z, scale, unk00, unk01, unk02, unk03, unk04, file_base, unk05, unk06, extra_info_array_flag, extra_info_array_length, extra_info_array\n")
        pos = tile_array_offset

        # read area_array
        for index in range(0, tile_array_length):
            # offset = tile_array_offset + index * 0x30
            offset = struct.unpack('>I', self.data[pos:pos + 0x04])[0] + pos
            pos += 0x04

            pos_x, pos_y, scale, unk00, unk01, unk02, unk03, unk04, file_base, unk05, unk06, extra_info_array_flag \
                = struct.unpack('>fffffffIIIII', self.data[offset:offset + 0x30])

            file_base = self.data[offset + file_base + 0x20:].split(b'\x00', 1)[0].decode('utf-8', 'strict')

            extra_info_array_length = 0
            extra_info_array = ()

            if extra_info_array_flag != 0:
                extra_info_array_length = struct.unpack('>I', self.data[offset + 0x30:offset + 0x34])[0]
                if extra_info_array_length == 8:
                    extra_info_array = struct.unpack('>IIIIIIII', self.data[offset + 0x34:offset + 0x54])
                elif extra_info_array_length == 4:
                    extra_info_array = struct.unpack('>IIII', self.data[offset + 0x34:offset + 0x44])
                else:
                    extra_info_array = ()

            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, \"{13}\"\n".format(pos_x, pos_y, scale, unk00, unk01, unk02, unk03, unk04, file_base, unk05, unk06, extra_info_array_flag, extra_info_array_length, str(extra_info_array)))
        file.close()


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild Terrain Scene file parser")
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

    tscb = TSCB(args.filename)

    exit(0)

    if args.all:
        args.yaml = True
        args.json = True
        args.xml = True

    if args.yaml:
        save_as_yaml(args, tscb)

    if args.json:
        save_as_json(args, tscb)

    if args.xml:
        save_as_xml(args, tscb)

    if not args.yaml and not args.json and not args.xml:
        save_as_yaml(args, tscb)


def save_as_yaml(args, tscb):
    filename = os.path.basename(args.filename)
    print('Saving {0}.yaml...'.format(filename))
    file = open(args.filename + '.yaml', 'w')
    file.write(yaml.dump(tscb.data_object))
    file.close()


def save_as_json(args, tscb):
    filename = os.path.basename(args.filename)
    print('Saving {0}.json...'.format(filename))
    file = open(args.filename + '.json', 'w')
    file.write(json.dumps(tscb.data_object))
    file.close()


def save_as_xml(args, tscb):
    from xml.dom.minidom import parseString

    filename = os.path.basename(args.filename)
    print('Saving {0}.xml...'.format(filename))
    file = open(args.filename + '.xml', 'w')
    dom = dicttoxml.dicttoxml(tscb.data_object).decode('utf-8')
    file.write(parseString(dom).toprettyxml())
    file.close()


if __name__ == "__main__":
    main()
