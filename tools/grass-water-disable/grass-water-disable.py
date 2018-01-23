import argparse
from shutil import copyfile
import os
import struct


def disable_tscb(path, is_water, is_grass, is_backup):
    print("Parsing Binary Terrain Scene file...")

    filename = os.path.basename(path)
    backup_path = path + '.bak'

    file = open(path, 'rb+')
    data = file.read()

    signature = data[0x00:0x04]

    if signature != b'TSCB':
        print('Quitting: {0} is not a valid TSCB file...'.format(filename))
        print('Expected b\'TSCB\' but saw {0}'.format(signature))
        exit(0)

    if is_backup:
        print('Saving a backup copy of original tscb...')
        if os.path.isfile(backup_path):
            backup_overwrite_prompt = ''
            while True:
                backup_overwrite_prompt = \
                    input("A backup of this tscb file already exists, would you like to overwrite it? (y/n) ")
                if backup_overwrite_prompt == 'y' or backup_overwrite_prompt == 'Y' \
                        or backup_overwrite_prompt == 'n' or backup_overwrite_prompt == 'N':
                    break

            if backup_overwrite_prompt == 'y' or backup_overwrite_prompt == 'Y':
                copyfile(path, backup_path)
        else:
            copyfile(path, backup_path)

    print("Reading {0}...".format(filename))

    # get size of area array
    file.seek(0x1c)
    area_array_length = struct.unpack('>I', file.read(0x04))[0]

    # get address of area array
    file.seek(0x30)
    area_array_offset = struct.unpack('>I', file.read(0x04))[0]
    file.seek(area_array_offset, 1)

    area_array_offsets = []

    # real list of addresses to area array entries
    for i in range(0, area_array_length):
        area_array_offsets.append(file.tell() + struct.unpack('>I', file.read(0x04))[0])

    # disable grass and / or water in area array
    for i in range(0, len(area_array_offsets)):
        # seek to area array entry
        file.seek(area_array_offsets[i])
        pos = file.tell()

        x, y, scale, area_min_height_ground, area_max_height_ground, area_min_height_water, area_max_height_water, \
        unk04, file_base, unk05, unk06, ref_extra, extra_info_array_length = \
            struct.unpack('>fffffffIIIIII', file.read(0x34))

        if 0 < extra_info_array_length <= 8:
            if is_water and is_grass:
                file.seek(pos)
                file.write(struct.pack('>fffffffIIIIII', x, y, scale, area_min_height_ground, area_max_height_ground, area_min_height_water, area_max_height_water, 0, file_base, unk05, unk06, 0, 0))
                continue

            if is_water:
                extra_info_array = []

                for index in range(0, extra_info_array_length):
                    extra_info_array.append(struct.unpack('>I', file.read(0x04))[0])

                if extra_info_array == [20, 3, 0, 1, 0, 3, 1, 1] or \
                        extra_info_array == [20, 3, 1, 1, 0, 3, 0, 1]:
                    file.seek(pos)
                    file.write(
                        struct.pack('>fffffffIIIIIIIIIIIIII', x, y, scale, area_min_height_ground, area_max_height_ground,
                                    area_min_height_water, area_max_height_water, 1, file_base, unk05, unk06, 4, 4, 3,
                                    0, 1, 0, 0, 0, 0, 0))

                elif extra_info_array == [3, 1, 1, 0]:
                    file.seek(pos)
                    file.write(
                        struct.pack('>fffffffIIIIII', x, y, scale, area_min_height_ground, area_max_height_ground,
                                    area_min_height_water, area_max_height_water, 0, file_base, unk05, unk06, 0, 0))

                continue

            if is_grass:
                extra_info_array = []

                for index in range(0, extra_info_array_length):
                    extra_info_array.append(struct.unpack('>I', file.read(0x04))[0])

                if extra_info_array == [20, 3, 0, 1, 0, 3, 1, 1] or \
                        extra_info_array == [20, 3, 1, 1, 0, 3, 0, 1]:
                    file.seek(pos)
                    file.write(
                        struct.pack('>fffffffIIIIIIIIIIIIII', x, y, scale, area_min_height_ground,
                                    area_max_height_ground,
                                    area_min_height_water, area_max_height_water, 1, file_base, unk05, unk06, 4, 4, 3,
                                    1, 1, 0, 0, 0, 0, 0))

                elif extra_info_array == [3, 0, 1, 0]:
                    file.seek(pos)
                    file.write(
                        struct.pack('>fffffffIIIIII', x, y, scale, area_min_height_ground, area_max_height_ground,
                                    area_min_height_water, area_max_height_water, 0, file_base, unk05, unk06, 0, 0))

                continue

    file.close()
    exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="The Legend of Zelda: Breath of the Wild Terrain Grass and Water Disabler")
    parser.add_argument("filename", type=str, help="File to be parsed.")
    args = parser.parse_args()

    water_prompt = ''
    while True:
        water_prompt = input("Disable water? (y/n) ")
        if water_prompt == 'y' or water_prompt == 'Y' \
                or water_prompt == 'n' or water_prompt == 'N':
            break

    grass_prompt = ''
    while True:
        grass_prompt = input("Disable grass? (y/n) ")
        if grass_prompt == 'y' or grass_prompt == 'Y' \
                or grass_prompt == 'n' or grass_prompt == 'N':
            break

    backup_prompt = ''
    while True:
        backup_prompt = input("Backup original tscb? (y/n) ")
        if backup_prompt == 'y' or backup_prompt == 'Y' \
                or backup_prompt == 'n' or backup_prompt == 'N':
            break

    is_water = True if water_prompt == 'y' or water_prompt == 'Y' else False
    is_grass = True if grass_prompt == 'y' or grass_prompt == 'Y' else False
    is_backup = True if backup_prompt == 'y' or backup_prompt == 'Y' else False

    disable_tscb(args.filename, is_water, is_grass, is_backup)

    exit(0)


if __name__ == "__main__":
    main()
