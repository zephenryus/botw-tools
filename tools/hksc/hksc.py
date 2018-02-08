import argparse
import json

import os
import struct

import datetime


class HKSC:
    def __init__(self, path):
        print("Parsing Havok Scene file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        file = open(path, 'rb')
        self.get_section(file)

        # end = file.read(0x01)
        # if end != b'\xff':
        #     print('Quitting: where is the padding?!')
        #     print(end)
        #     print(hex(file.tell()))
        exit(0)

    def get_section(self, file, offset=0):
        print('Reading section...')
        file.seek(offset)
        signature = file.read(0x08)

        if signature != b'\x57\xE0\xE0\x57\x10\xC0\xC0\x10':
            print('Quitting: Invalid file signature')
            print('Expected b\'\\x57\\xE0\\xE0\\x57\\x10\\xC0\\xC0\\x10\' but saw {0}'.format(signature))
            exit(0)

        version, unk01, bom, unk02, unk03, section_count, unk04, unk05 = \
            struct.unpack('>xxxxIBBBBIIxxxxxxxxI', file.read(0x20))
        # print(version, unk01, bom, unk02, unk03, section_count, unk04, unk05)

        version_name = file.read(0x10).split(b'\x00')[0]
        # print(version_name.decode('utf-8'))

        unk_offset = struct.unpack('>xxxxHH', file.read(0x08))
        if unk_offset[1] != 0:
            file.seek(-0x08, 1)
            unk_offset = struct.unpack('>xxxxHHHxxxxxxxxxxxxxx', file.read(0x18))

        sections = []

        csv_name = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S.%f') + '-sections.csv'
        csv = open(csv_name, 'w')
        csv.write('name, start_offset, unk_offset0, unk_offset1, unk_offset2, unk_offset3, unk_offset4, size\n')

        for index in range(0, section_count):
            section = {
                'section_name': file.read(0x14).split(b'\x00')[0],
                'section_start': struct.unpack('>I', file.read(0x04))[0],
                'offset_1': struct.unpack('>I', file.read(0x04))[0],
                'offset_2': struct.unpack('>I', file.read(0x04))[0],
                'offset_3': struct.unpack('>I', file.read(0x04))[0],
                'offset_4': struct.unpack('>I', file.read(0x04))[0],
                'offset_5': struct.unpack('>I', file.read(0x04))[0],
                'section_size': struct.unpack('>I', file.read(0x04))[0]
            }

            csv.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n'
                      .format(
                section['section_name'].decode('utf-8'),
                hex(section['section_start']),
                hex(section['offset_1']),
                hex(section['offset_2']),
                hex(section['offset_3']),
                hex(section['offset_4']),
                hex(section['offset_5']),
                hex(section['section_size'])
            ))

            file.seek(0x10, 1)
            sections.append(section)

        csv.close()

        print(sections)

        # Get classnames
        if sections[0]['section_name'] == b'__classnames__':
            classnames = self.get_classnames(file, sections[0]['section_start'] + offset, sections[0]['section_size'])
            # print(classnames)

        if sections[1]['section_start'] != sections[2]['section_start']:
            print('Quitting: types and data headers start at different offsets')
            print('types offset: {0}, data offset: {1}'
                  .format(hex(sections[1]['section_start']), hex(sections[2]['section_start'])))
            exit(0)

        file.seek(sections[1]['section_start'] + offset)

        next_file_offset, types_count, data_count = \
            struct.unpack('>IxxxxIxxxxxxxxIxxxxxxxx', file.read(0x20))

        types_offset = offset + sections[1]['section_start'] + 0x20
        data_offset = offset + types_offset + types_count * 0x10

        print(hex(types_offset))
        types = self.get_types(file, types_offset, types_count)
        data = self.get_data(file, data_offset, data_count)

        for index in range(len(types)):
            type = types[index]
            type_data = []

            for data_index in range(type['DataIndexStart'], type['DataIndexEnd']):
                type_datas = data[data_index]
                type_data.append({
                    'unk0': type_datas['unk0'],
                    'unk1': type_datas['unk1'],
                    'unk2': type_datas['unk2'],
                    'unk3': type_datas['unk3']
                })

            types[index]['data'] = type_data

        json_name = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S.%f') + '-section-data.json'
        json_file = open(json_name, 'w')
        json_file.write(json.dumps(types, sort_keys=True, indent=4, separators=(',', ': ')))
        # print(types)

        if next_file_offset != 0:
            self.get_section(file, next_file_offset)

    def get_classnames(self, file, offset, size):
        print('Reading classnames...')
        file.seek(offset)
        classnames = []

        csv_name = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S.%f') + '-classnames.csv'
        csv = open(csv_name, 'w')
        csv.write('id, name\n')

        while file.tell() < offset + size:
            if file.read(0x01) == b'\xff':
                break
            file.seek(-0x01, 1)

            classname = {
                'id': hex(struct.unpack('>I', file.read(0x04))[0]),
                'name': readString(file)
            }
            csv.write('{0}, {1}\n'.format(classname['id'], classname['name'].decode('utf-8')))

            classnames.append(classname)

        csv.close()
        return classnames

    def get_types(self, file, pos, count):
        print('Reading types...')
        types = []
        file.seek(pos, 0)

        csv_name = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S.%f') + '-types.csv'
        csv = open(csv_name, 'w')
        csv.write('HashId, SRTHash, DataIndexStart, DataIndexEnd\n')

        for index in range(0, count):
            type = {
                'HashId': struct.unpack('>I', file.read(0x04))[0],
                'SRTHash': struct.unpack('>I', file.read(0x04))[0],
                'DataIndexStart': struct.unpack('>I', file.read(0x04))[0],
                'DataIndexEnd': struct.unpack('>I', file.read(0x04))[0]
            }

            types.append(type)
            csv.write('{0}, {1}, {2}, {3}\n'.format(
                type['HashId'],
                type['SRTHash'],
                type['DataIndexStart'],
                type['DataIndexEnd']
            ))

        return types

    def get_data(self, file, pos, count):
        print('Reading data...')
        datas = []
        file.seek(pos, 0)

        csv_name = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S.%f') + '-data.csv'
        csv = open(csv_name, 'w')
        csv.write('unk0, unk1, unk2, unk3\n')

        for index in range(0, count):
            data = {
                'unk0': struct.unpack('>I', file.read(0x04))[0],
                'unk1': struct.unpack('>I', file.read(0x04))[0],
                'unk2': struct.unpack('>H', file.read(0x02))[0],
                'unk3': struct.unpack('>H', file.read(0x02))[0]
            }

            datas.append(data)
            csv.write('{0}, {1}, {2}, {3}\n'.format(
                data['unk0'],
                data['unk1'],
                data['unk2'],
                data['unk3']
            ))

        return datas


def readString(file):
    string = []

    while True:
        character = file.read(0x01)

        if character == b'\x00':
            return b''.join(string)
        string.append(character)


def main():
    parser = argparse.ArgumentParser(
        description="The Legend of Zelda: Breath of the Wild Havok Scene Parser")
    # parser.add_argument("filename", type=str, help="File to be parsed.")
    args = parser.parse_args()

    filename = "C:\\botw-data\\decompressed\\content\\Physics\\StaticCompound\\MainField\\E-4-1.hksc"

    HKSC(filename)


if __name__ == "__main__":
    main()
