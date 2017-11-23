import argparse
import sys
import os
from PIL import Image


class HGHT:
    def __init__(self, path, is_terrain, is_water, is_material, is_grass, is_composite, is_gray_scale):
        print("Extracting HGHT...")

        terrain_height_map_gradient = [
            [0.00, 0x00, 0x9a, 0x24],
            [0.45, 0xff, 0xff, 0x00],
            [0.90, 0xff, 0x00, 0x00],
            [1.00, 0xff, 0xa0, 0xa0]
        ]

        water_height_map_gradient = [
            [0.00, 0x34, 0x40, 0x44],
            [1.00, 0x15, 0x54, 0xd1]
        ]

        water_depth_map_gradient = [
            [0.00, 0x15, 0x54, 0xd1],
            [1.00, 0x34, 0x40, 0x44]
        ]

        grass_map_gradient = [
            [0.06, 0x00, 0xff, 0xff],
            [0.11, 0x00, 0xff, 0x00],
            [0.17, 0xff, 0xff, 0x00],
            [0.22, 0xff, 0x00, 0x00],
            [0.28, 0xff, 0x00, 0xff],
            [0.33, 0x00, 0x00, 0xff],
            [0.39, 0x00, 0xff, 0xff],
            [0.44, 0x00, 0xff, 0x00],
            [0.50, 0xff, 0xff, 0x00],
            [0.56, 0xff, 0x00, 0x00],
            [0.61, 0xff, 0x00, 0xff],
            [0.67, 0x00, 0x00, 0xff],
            [0.72, 0x00, 0xff, 0xff],
            [0.78, 0x00, 0xff, 0x00],
            [0.83, 0xff, 0xff, 0x00],
            [0.89, 0xff, 0x00, 0x00],
            [0.94, 0xff, 0x00, 0xff],
            [1.00, 0x00, 0x00, 0xff]
        ]

        mate_map_gradient = [
            [0.00, 0xff, 0x00, 0x00],
            [0.08, 0xff, 0x00, 0xff],
            [0.14, 0x00, 0x00, 0xff],
            [0.21, 0x00, 0xff, 0xff],
            [0.29, 0x00, 0xff, 0x00],
            [0.36, 0xff, 0xff, 0x00],
            [0.43, 0xff, 0x00, 0x00],
            [0.50, 0xff, 0x80, 0x80],
            [0.58, 0xff, 0x80, 0xff],
            [0.64, 0x80, 0x80, 0xff],
            [0.71, 0x80, 0xff, 0xff],
            [0.79, 0x80, 0xff, 0x80],
            [0.86, 0xff, 0xff, 0x80],
            [1.00, 0xff, 0x80, 0x80],
        ]

        gray_scale_gradient = [
            [0.00, 0x00, 0x00, 0x00],
            [1.00, 0xff, 0xff, 0xff]
        ]

        filename = os.path.splitext(path)[0]
        size = 0x100

        if is_gray_scale:
            terrain_height_map_gradient = gray_scale_gradient
            water_height_map_gradient = gray_scale_gradient
            # water_depth_map_gradient = gray_scale_gradient
            grass_map_gradient = gray_scale_gradient
            mate_map_gradient = gray_scale_gradient

        if is_terrain:
            if os.path.isfile(filename + ".hght"):
                self.create_map(filename, ".hght", size, terrain_height_map_gradient, 0, 1)
            else:
                print("\033[93mSkipping " + filename + ".hght because it does not exist\033[0m")

        if is_water:
            if os.path.isfile(filename + ".water.extm"):
                self.create_map(filename, ".water.extm", size, water_height_map_gradient, 6, 4)
            else:
                print("\033[93mSkipping " + filename + ".water.extm because it does not exist\033[0m")

        if is_grass:
            if os.path.isfile(filename + ".grass.extm"):
                self.create_map(filename, ".grass.extm", size, grass_map_gradient, 2, 4)
            else:
                print("\033[93mSkipping " + filename + ".grass.extm because it does not exist\033[0m")

        if is_material:
            if os.path.isfile(filename + ".mate"):
                self.create_map(filename, ".mate", size, mate_map_gradient, 2, 1)
            else:
                print("\033[93mSkipping " + filename + ".mate because it does not exist\033[0m")

        if is_composite:
            if os.path.isfile(filename + ".hght") and os.path.isfile(filename + ".water.extm"):
                self.create_composite_map(filename, terrain_height_map_gradient, water_depth_map_gradient)
            else:
                print("\033[93mSkipping composite because .hght or .water.extm do not exist\033[0m")

        return

    def create_map(self, filename, extension=".hght", size=0x100, gradient=None, padding=0, block_size=1):
        if gradient is None:
            gradient = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        print("Reading " + os.path.basename(filename) + extension + " data...")
        data = open(filename + extension, 'rb')
        height_map = self.get_height_map(data, 0xffff, size, padding, block_size)

        print("Creating " + os.path.basename(filename) + extension + " map...")
        map_image = self.get_height_map_image(height_map, size, gradient)

        print("Saving " + os.path.basename(filename) + extension + ".png...")
        directory = os.path.dirname(filename + extension) + "\\maps\\"
        if not os.path.exists(directory):
            os.makedirs(directory)
        map_image.save(directory + os.path.basename(filename) + extension + ".png")

    @staticmethod
    def get_height_map(data, height_max=0xffff, size=0x100, padding=0, block_size=1):
        height_map = [any] * size * size

        for y in range(0, int(size / block_size)):
            for x in range(0, int(size / block_size)):
                height = int.from_bytes(data.read(2), 'little')
                data.read(padding)

                for y2 in range(0, block_size):
                    for x2 in range(0, block_size):
                        height_map[(y * block_size + y2) * size + x * block_size + x2] = height / height_max

        return height_map

    def get_height_map_image(self, height_map, size=0x100, color_gradient=None):
        height_map_image = Image.new("RGB", (size, size))

        if color_gradient is None:
            color_gradient = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        for y in range(0, size):
            for x in range(0, size):
                height = height_map[y * size + x]

                color = self.lerp_rgb(self.get_height_color(height, color_gradient), height)
                height_map_image.putpixel((x, y), color)

        return height_map_image

    def create_composite_map(self, filename, terrain_gradient, water_gradient):
        size = 0x100
        composite_map_image = Image.new("RGB", (size, size))

        print("Reading composite data...")
        terrain = open(filename + '.hght', 'rb')
        water = open(filename + '.water.extm', 'rb')

        print("Creating composite map...")
        terrain_height_map = self.get_height_map(terrain, 0xffff, size, 0, 1)
        water_height_map = self.get_height_map(water, 0xffff, size, 6, 4)

        for y in range(0, size):
            for x in range(0, size):
                terrain_height = terrain_height_map[y * size + x]
                water_height = water_height_map[y * size + x]

                if water_height > terrain_height:
                    depth = water_height - terrain_height
                    color = self.lerp_rgb(self.get_height_color(depth, water_gradient), depth)
                else:
                    color = self.lerp_rgb(self.get_height_color(terrain_height, terrain_gradient), terrain_height)
                composite_map_image.putpixel((x, y), color)

        print("Saving " + os.path.basename(filename) + ".composite.png...")
        directory = os.path.dirname(filename + '.hght') + "\\maps\\"
        if not os.path.exists(directory):
            os.makedirs(directory)

        composite_map_image.save(directory + os.path.basename(filename) + ".composite.png")

    @staticmethod
    def lerp_rgb(color_range_data, t):
        t = t / color_range_data[1][0]
        return (
            (int(color_range_data[0][1] + (color_range_data[1][1] - color_range_data[0][1]) * t)),
            (int(color_range_data[0][2] + (color_range_data[1][2] - color_range_data[0][2]) * t)),
            (int(color_range_data[0][3] + (color_range_data[1][3] - color_range_data[0][3]) * t))
        )

    @staticmethod
    def get_height_color(height, gradient):
        current_color = (0, 0, 0, 0)
        last_color = (0, 0, 0, 0)

        for index in range(0, len(gradient)):
            last_color = current_color
            current_height = gradient[index][0]
            current_color = (
                current_height,
                gradient[index][1],
                gradient[index][2],
                gradient[index][3],
            )

            if height < gradient[index][0]:
                break

        return last_color, current_color


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

    HGHT(args.filename, image_types[0], image_types[1], image_types[2], image_types[3], image_types[4], image_types[5])

    sys.exit(1)


if __name__ == "__main__":
    main()
