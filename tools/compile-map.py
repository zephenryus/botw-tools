import os
import struct

import sys

from PIL import Image


def main():
    extensions = [
        'composite',
        'grass.extm',
        'hght',
        'mate',
        'water.extm'
    ]

    for extension in enumerate(extensions):
        old_map = Image.new('RGB', (256, 256))

        for zoom in range(0, 9):
            print('Compiling /compiled/5{0}00000000.{1}.png...'.format(zoom, extension[1]))
            count = 4 ** zoom
            image_width = 2 ** zoom * 256

            current_map = Image.new('RGB', (image_width, image_width))
            old_map = old_map.resize((image_width, image_width), Image.NEAREST)
            current_map.paste(old_map, (0, 0, image_width, image_width))

            for tile in range(0, count):
                print("Progress: %d%%" % ((tile + 1) / count * 100))
                path = 'C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5{0}00000000\\maps\\5{0}0000{2}.{1}.png'.format(
                    zoom, extension[1], '{:04x}'.format(tile))
                if os.path.isfile(path):
                    currentTile = Image.open(path)
                    pos = get_mdb_position(tile)
                    current_map.paste(currentTile, (pos[0] * 256, pos[1] * 256, pos[0] * 256 + 256, pos[1] * 256 + 256))
            current_map.save(os.path.expanduser(
                'C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\compiled\\5{0}00000000.{1}.png'.format(
                    zoom, extension[1])))
            old_map = current_map
    sys.exit(1)


# Lookup for Moser-de Bruijn Sequence
def get_mdb_position(value):
    if value <= 0:
        return 0, 0
    value = int(value)
    x = 0
    y = 0
    mask = 1
    offset = 0
    maxInt = 2 ** (struct.Struct('i').size * 8 - 1) - 1

    while True:
        x |= value >> offset & mask
        offset += 1
        y |= value >> offset & mask
        mask <<= 1
        if value < 1 << offset + 1 or mask > maxInt:
            break
    return x, y


if __name__ == "__main__":
    main()
