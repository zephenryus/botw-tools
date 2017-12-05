import argparse
import sys
import os

from PIL import Image

# import src.extractors.gradientmaps as gradient_maps
import gradientmaps as gradient_maps


class HGHT:
    COLOR_MODE_GRADIENT = 0x00
    COLOR_MODE_TABLE = 0x01
    COLOR_MODE_VALUE = 0x02

    maps = {
        "terrain": {
            "data_length": 2,
            "padding": 0,
            "block_size": 1,
            "size": 0x100,
            "height_max": 0xffff,
            "extension": ".hght",
            "color_table": gradient_maps.Terrain,
            # "color_table": gradient_maps.GrayScale,
            "color_mode": COLOR_MODE_VALUE
            # "color_mode": COLOR_MODE_GRADIENT
        },
        "water": {
            "data_length": 2,
            "padding": 6,
            "block_size": 4,
            "size": 0x100,
            "height_max": 0xffff,
            "extension": ".water.extm",
            "color_table": gradient_maps.Water,
            "color_mode": COLOR_MODE_GRADIENT
        },
        # self.create_map(filename, ".mate", 4, size, mate_map_gradient, 0, 1, self.COLOR_MODE_TABLE)
        "material": {
            "data_length": 4,
            "padding": 0,
            "block_size": 1,
            "size": 0x100,
            "height_max": 0x01,
            "extension": ".mate",
            "color_table": None,
            "color_mode": COLOR_MODE_VALUE
        },
        # self.create_map(filename, ".grass.extm", 2, size, grass_map_gradient, 2, 4)
        "grass": {
            "data_length": 4,
            "padding": 0,
            "block_size": 4,
            "size": 0x100,
            "height_max": 0x01,
            "extension": ".grass.extm",
            "color_table": None,
            "color_mode": COLOR_MODE_VALUE
        },

    }

    def __init__(self, path, flags):
        print("Extracting HGHT...")

        is_terrain = flags[0]
        is_water = flags[1]
        is_material = flags[2]
        is_grass = flags[3]
        is_composite = flags[4]
        is_gray_scale = flags[5]

        filename = os.path.splitext(path)[0]
        size = 0x100

        # if is_gray_scale:
        # terrain_height_map_gradient = gray_scale_gradient
        # water_height_map_gradient = gray_scale_gradient
        # water_depth_map_gradient = gray_scale_gradient
        # grass_map_gradient = gray_scale_gradient
        # mate_map_gradient = gray_scale_gradient

        index = 0
        for key, botwMap in self.maps.items():
            if flags[index]:
                if os.path.isfile(filename + botwMap['extension']):
                    self.create_map(filename, botwMap['data_length'], botwMap['padding'], botwMap['block_size'],
                                    botwMap['size'], botwMap['height_max'], botwMap['extension'],
                                    botwMap['color_table'], botwMap['color_mode'])
                else:
                    print("\033[93mSkipping " + filename + botwMap['extension'] + " because it does not exist\033[0m")
            index += 1

        if is_composite:
            if os.path.isfile(filename + ".hght") and os.path.isfile(filename + ".water.extm"):
                self.create_composite_map(filename, gradient_maps.Terrain, gradient_maps.WaterDepth)
            else:
                print("\033[93mSkipping composite because .hght or .water.extm do not exist\033[0m")

        return

    def create_map(self, filename, data_length=1, padding=0, block_size=1, size=0x100, height_max=0xffff,
                   extension=".hght", gradient=None, color_mode=None):
        if gradient is None:
            gradient = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        if color_mode is None:
            color_mode = self.COLOR_MODE_VALUE

        print("Reading " + os.path.basename(filename) + extension + " data...")
        data = open(filename + extension, 'rb')
        height_map = self.get_height_map(data, data_length, size, padding, block_size)

        print("Rendering " + os.path.basename(filename) + extension + " map...")
        map_image = self.render_height_map_image(height_map, size, gradient, color_mode, height_max)

        directory = os.path.dirname(filename + extension) + "\\maps\\"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # if color_mode is self.COLOR_MODE_VALUE:
        #     print("Saving maps/" + os.path.basename(filename) + extension + ".jpg...")
        #     map_image.save(directory + os.path.basename(filename) + extension + ".jpg", "jpeg", quality=100,
        #                    optimize=False)
        # else:
        print("Saving maps/" + os.path.basename(filename) + extension + ".png...")
        map_image.save(directory + os.path.basename(filename) + extension + ".png")

    @staticmethod
    def get_height_map(data, read_bytes=2, size=0x100, padding=0, block_size=1):
        height_map = [any] * size * size

        for y in range(0, int(size / block_size)):
            for x in range(0, int(size / block_size)):
                height = int.from_bytes(data.read(read_bytes), 'little')
                data.read(padding)

                for y2 in range(0, block_size):
                    for x2 in range(0, block_size):
                        height_map[(y * block_size + y2) * size + x * block_size + x2] = height

        return height_map

    def render_height_map_image(self, height_map, size=0x100, color_table=None, color_mode=None, height_max=0xffff):
        if color_mode is None:
            color_mode = self.COLOR_MODE_VALUE

        if color_mode is self.COLOR_MODE_VALUE:
            height_map_image = Image.new("RGBA", (size, size))
        else:
            height_map_image = Image.new("RGB", (size, size))

        if color_table is None:
            color_table = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        for y in range(0, size):
            for x in range(0, size):
                height = height_map[y * size + x]

                if color_mode == self.COLOR_MODE_TABLE:
                    color = self.lookup_color_table(height, color_table)
                elif color_mode == self.COLOR_MODE_GRADIENT:
                    color = self.lerp_rgb(self.get_height_color(height / height_max, color_table), height / height_max)
                else:
                    color = self.value_to_color(height)

                height_map_image.putpixel((x, y), color)

        return height_map_image

    def create_composite_map(self, filename, terrain_gradient, water_gradient):
        size = 0x100
        composite_map_image = Image.new("RGB", (size, size))

        print("Reading composite data...")
        terrain = open(filename + '.hght', 'rb')
        water = open(filename + '.water.extm', 'rb')

        print("Creating composite map...")
        terrain_height_map = self.get_height_map(terrain, 2, size, 0, 1)
        water_height_map = self.get_height_map(water, 2, size, 6, 4)

        for y in range(0, size):
            for x in range(0, size):
                terrain_height = float(terrain_height_map[y * size + x] / 0xffff)
                water_height = float(water_height_map[y * size + x] / 0xffff)

                if water_height >= terrain_height:
                    depth = water_height - terrain_height
                    color = self.lerp_rgb(self.get_height_color(depth, gradient_maps.WaterDepth), depth)
                else:
                    color = self.lerp_rgb(self.get_height_color(terrain_height, gradient_maps.Terrain), terrain_height)
                composite_map_image.putpixel((x, y), color)

        print("Saving " + os.path.basename(filename) + ".composite.png...")
        directory = os.path.dirname(filename + '.hght') + "\\maps\\"
        if not os.path.exists(directory):
            os.makedirs(directory)

        composite_map_image.save(directory + os.path.basename(filename) + ".composite.png", "PNG")

    @staticmethod
    def lerp_rgb(color_range_data, t):
        t = (t - color_range_data[0][0]) / (color_range_data[1][0] - color_range_data[0][0])
        return (
            (int((1 - t) * color_range_data[0][1] + t * color_range_data[1][1])),
            (int((1 - t) * color_range_data[0][2] + t * color_range_data[1][2])),
            (int((1 - t) * color_range_data[0][3] + t * color_range_data[1][3]))
        )

    @staticmethod
    def get_height_color(height, gradient):
        current_color = (0, 0, 0, 0)
        last_color = (0, 0, 0, 0)

        for index in range(0, len(gradient)):
            last_color = current_color
            current_height = gradient[index]['stop']
            current_color = (
                current_height,
                gradient[index]['color']['r'],
                gradient[index]['color']['g'],
                gradient[index]['color']['b']
            )

            if height < gradient[index]['stop']:
                break

        return last_color, current_color

    @staticmethod
    def lookup_color_table(value, color_table):
        value = int(value)
        return color_table[value]

    @staticmethod
    def value_to_color(value):
        value = int(value)
        r = value >> 0 & 0xff
        g = value >> 8 & 0xff
        b = value >> 16 & 0xff
        a = value >> 24 & 0xff
        a = 0xff

        return r, g, b, a
        # return r, g, b


def main():
    parser = argparse.ArgumentParser(description="Parse the Legend of Zelda: Breath of the Wild terrain files to png")
    parser.add_argument("filename", type=str, help="File to be parsed.")
    parser.add_argument("-a", "--all",
                        help="Generate all map types. Terrain height map, water height map, material map, grass map " +
                             "and terrain and water composite map",
                        action="store_true")
    parser.add_argument("-t", "--terrain",
                        help="Generate terrain height map",
                        action="store_true")
    parser.add_argument("-w", "--water",
                        help="Generate water height map",
                        action="store_true")
    parser.add_argument("-m", "--material",
                        help="Generate material map",
                        action="store_true")
    parser.add_argument("-g", "--grass",
                        help="Generate grass map",
                        action="store_true")
    parser.add_argument("-c", "--composite",
                        help="Generate terrain and water composite map",
                        action="store_true")
    parser.add_argument("-gs", "--grayscale",
                        help="Generate as gray scale map",
                        action="store_true")
    args = parser.parse_args()

    image_types = (False, False, False, False, False, False)

    if args.terrain:
        image_types = (True, image_types[1], image_types[2], image_types[3], image_types[4], image_types[5])

    if args.water:
        image_types = (image_types[0], True, image_types[2], image_types[3], image_types[4], image_types[5])

    if args.material:
        image_types = (image_types[0], image_types[1], True, image_types[3], image_types[4], image_types[5])

    if args.grass:
        image_types = (image_types[0], image_types[1], image_types[2], True, image_types[4], image_types[5])

    if args.composite:
        image_types = (image_types[0], image_types[1], image_types[2], image_types[3], True, image_types[5])

    if args.grayscale:
        image_types = (image_types[0], image_types[1], image_types[2], image_types[3], image_types[4], True)

    if args.all:
        image_types = (True, True, True, True, True, image_types[5])

    if not args.all and not args.terrain and not args.water and not args.material and not args.grass \
            and not args.composite:
        image_types = (True, True, True, True, True, image_types[5])

    HGHT(
        args.filename,
        image_types
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
