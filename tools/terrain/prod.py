import argparse
import codecs
import json

import os
import struct

import dicttoxml
import yaml


class PrOD:
    data_object = {}

    def __init__(self, path, temp_data=None):
        print("Parsing PrOD file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        try:
            file = open(path, 'rb')
            self.data = file.read()
        except PermissionError:
            self.data = temp_data

        signature = self.data[0x00:0x04]

        if signature != b'PrOD':
            print('\033[31mQuitting: {0} is not a PrOD file\033[0m'.format(filename))
            print('\033[31mExpected b\'AAMP\' but saw {0}\033[0m'.format(signature))
            exit(0)

        # I'm not completely sure this is the version, since it is little-endian and the rest
        # of the file is big-endian.
        version = struct.unpack('<I', self.data[0x04:0x08])[0]

        if version != 1:
            print('\033[31mQuitting: {0} is not the correct PrOD version\033[0m'.format(filename))
            print('\033[31mExpected 1 but saw {0}\033[0m'.format(version))
            exit(0)

        count, length = struct.unpack('>II', self.data[0x08:0x10])

        filesize, cluster_count, strings_ptr = \
            struct.unpack('>III', self.data[0x10:0x1c])

        pos = 0x20
        for _ in range(cluster_count):
            cluster_size, element_count, cluster_strptr = \
                struct.unpack('>III', self.data[pos:pos + 0x0c])
            name = self.data[strings_ptr + cluster_strptr:].split(b'\0')[0].decode('utf-8')
            name = str(name)

            self.data_object[name] = {}
            for j in range(element_count):
                # Model/%s.bfres
                # Model/%s.Tex2.bfres
                x, y, z, rot_x, rot_y, rot_z, scale = \
                    struct.unpack('>fffffff', self.data[pos + 0x10 + j * 0x20:pos + 0x2c + j * 0x20])
                self.data_object[name]['X'] = x
                self.data_object[name]['Y'] = y
                self.data_object[name]['Z'] = z
                self.data_object[name]['RotX'] = rot_x
                self.data_object[name]['RotY'] = rot_y
                self.data_object[name]['RotZ'] = rot_z
                self.data_object[name]['Scale'] = scale
            pos += 0x10 + cluster_size


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

    prod = PrOD(args.filename)

    if args.all:
        args.yaml = True
        args.json = True
        args.xml = True

    if args.yaml:
        save_as_yaml(args, prod)

    if args.json:
        save_as_json(args, prod)

    if args.xml:
        save_as_xml(args, prod)

    if not args.yaml and not args.json and not args.xml:
        save_as_xml(args, prod)


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
    print('Saving {0}...'.format(args.filename + '.xml'))
    file = codecs.open(args.filename + '.xml', 'w', 'utf-8')
    dom = dicttoxml.dicttoxml(byml.data_object).decode('utf-8')
    file.write(parseString(dom).toprettyxml())
    file.close()


if __name__ == "__main__":
    main()
