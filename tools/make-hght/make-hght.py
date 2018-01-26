import argparse

import os
import struct

from PIL import Image


def main():
    parser = argparse.ArgumentParser(
        description="The Legend of Zelda: Breath of the Wild hght maker")
    parser.add_argument("filename", type=str, help="Image file to use to generate hght files.")
    args = parser.parse_args()

    image = Image.open(args.filename)
    image.thumbnail((256, 256), Image.ANTIALIAS)
    image.save(os.path.splitext(args.filename)[0] + '.256.png', 'png')

    image = Image.open(os.path.splitext(args.filename)[0] + '.256.png')
    rgb = image.convert('RGB')
    image_width, image_height = image.size
    heightmap = []

    hght = open('5000000000.hght.hex', 'wb+')

    for x in range(0, image_width):
        for y in range(0, image_height):
            r, g, b = rgb.getpixel((y, x))
            height = int(r / 255 * 0xffff)
            heightmap.append(height)
            hght.write(struct.pack('>H', height))


if __name__ == "__main__":
    main()
