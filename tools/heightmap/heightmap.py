import argparse

import os
import struct
import tempfile

import png
from PIL import Image


class Heightmap:
    def __init__(self, path):
        print('Reading Terrain Scene file...')

        self.base_path = os.path.dirname(os.path.realpath(path)) + '\\MainField\\'
        self.output_path = os.path.dirname(os.path.realpath(__file__)) + '\\heightmaps\\'

        tscb_filename = os.path.basename(path)

        with open(path, 'rb') as tscb:
            if tscb.read(0x04) != b'TSCB':
                print('Quitting: {0} is not a Terrain Scene file'.format(tscb_filename))
                exit(0)

            tscb.seek(0x1c)
            area_array_length = struct.unpack('>I', tscb.read(0x04))[0]

            tscb.seek(0x30)
            area_array_offset = tscb.tell() + struct.unpack('>I', tscb.read(0x04))[0]

            tscb.seek(0x28)
            self.world_scale = struct.unpack('>f', tscb.read(0x04))[0]

            self.area_array = self.get_area_array(tscb, area_array_offset, area_array_length)

            self.generate_heightmaps()

    @staticmethod
    def get_area_array(tscb, area_array_offset, area_array_length):
        area_array = []

        tscb.seek(area_array_offset)

        for index in range(0, area_array_length):
            offset = tscb.tell() + struct.unpack('>I', tscb.read(0x04))[0]
            resume_addr = tscb.tell()

            tscb.seek(offset)
            pos_x, pos_z, scale, area_min_height_ground, area_max_height_ground, area_min_height_water, \
            area_max_height_water, unk04, file_base, unk05, unk06, ref_extra \
                = struct.unpack('>fffffffIIIII', tscb.read(0x30))

            tscb.seek(offset + file_base + 0x20)
            file_base_name = tscb.read().split(b'\x00', 1)[0].decode('utf-8', 'strict')

            area_array.append({
                'x': pos_x,
                'z': pos_z,
                'scale': scale,
                'file_base': file_base_name
            })

            tscb.seek(resume_addr)

        return area_array

    def generate_heightmaps(self):
        current_scale = 0
        current_file_base = ''
        image_size = 0x100
        heightmap_image = Image.new("P", (image_size, image_size))

        for index in range(0, len(self.area_array)):
            base_file = self.area_array[index]['file_base']
            base_file_int = int(base_file, 16)
            base_dir = format(base_file_int - base_file_int % 0x04, 'x').upper() + '.hght\\'

            previous_scale = current_scale
            previous_file_base = current_file_base
            current_scale = self.area_array[index]['scale']
            current_file_base = self.area_array[index]['file_base']

            heightmap = []

            if os.path.isfile(self.base_path + base_dir + base_file + '.hght'):
                if previous_scale != current_scale and previous_file_base != '':
                    self.save_image(current_scale, heightmap, previous_file_base)

                    # heightmap_image.save(self.output_path + '5' + file_base_index + '00000000.hght.png', 'PNG', bits=7)

                    # with open(self.output_path + 'tmp.png', 'wb') as f:
                    #     writer = png.Writer(width=256, height=256, bitdepth=16, greyscale=True)
                    #     print(heightmap)
                    #     writer.write(f, heightmap)

                    new_size = (heightmap_image.size[0] * 2, heightmap_image.size[1] * 2)
                    heightmap_image = heightmap_image.resize(new_size, Image.NEAREST)

                    # heightmap_image = self.scale_heightmap_image(heightmap_image)

                heightmap = self.get_heightmap(self.base_path + base_dir + base_file + '.hght')
                self.render_heightmap(heightmap, heightmap_image, self.area_array[index])

            elif os.path.isfile(self.base_path + base_file + '.hght.sstera'):
                print('¯\_(ツ)_/¯ Sorry! SARC Extraction is not currently supported. It is planned for a future\n'
                      'release. You will have to extract the file with another tool. Try BotWUnpacker at\n'
                      'https://github.com/Shadsterwolf/BotWUnpacker')
                exit(0)

            else:
                print('Skipping {0}. It does not exist.'.format(base_file + '.hght'))

    def save_image(self, current_scale, heightmap, previous_file_base):
        file_base_index = previous_file_base[1]

        try:
            os.stat(self.output_path)
        except:
            os.mkdir(self.output_path)

        print('Saving 5{0}00000000.hght.png...'.format(file_base_index))
        print(heightmap)
        png.from_array(heightmap, 'L', {'bitdepth': 16}) \
            .save(self.output_path + '5' + file_base_index + '00000000.hght.png')

    def get_heightmap(self, path, size=0x100):
        heightmap = []
        row = []

        if os.path.isfile(path):
            filename = os.path.basename(path)
            print('Reading {0}...'.format(filename))

            with open(path, 'rb') as hght_file:
                for y in range(0, size):
                    row = []
                    for x in range(0, size):
                        height = struct.unpack('<H', hght_file.read(0x02))[0]
                        row.append([height])
                        # heightmap.append(height & 0xffff)
                    heightmap.append(row)

                heightmap.append(row)

        return heightmap

    def render_heightmap(self, heightmap, image, area, size=0x100):
        offset_x = int((((area['x'] + 16) - (area['scale'] / 2)) / area['scale']) * 256)
        offset_z = int((((area['z'] + 16) - (area['scale'] / 2)) / area['scale']) * 256)

        for z in range(0, size):
            for x in range(0, size):
                height = heightmap[z * size + x]
                r = int(height * 255) & 0xff
                g = int(height * 255) & 0xff
                b = int(height * 255) & 0xff

                image.putpixel((offset_x + x, offset_z + z), (r, g, b))

    def scale_heightmap_image(self, image):
        size = (image.size[0] * 2, image.size[1] * 2)
        image = image.resize(size, Image.NEAREST)
        return image


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild Heightmap Maker")
    parser.add_argument("filename", type=str, help="TSCB file")

    args = parser.parse_args()

    Heightmap(args.filename)

    exit(1)


if __name__ == "__main__":
    main()
