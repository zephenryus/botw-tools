import math

import sys
from time import gmtime, time

from PIL import Image


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.length = math.sqrt(x * x + y * y + z * z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Vector3(self.x, self.y, self.z)

    def __xor__(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def cross(self, other):
        return self ^ other

    def normalize(self):
        return Vector3(
            self.x / self.length,
            self.y / self.length,
            self.z / self.length,
        )

    def __str__(self):
        return "(x: {0}, y: {1}, z: {2})".format(self.x, self.y, self.z)


def main():
    angle = 166
    altitude = 75
    shadow_decay_length = 64

    sun = Vector3(
        math.cos(math.radians(angle)),
        math.sin(math.radians(altitude)),
        math.sin(math.radians(angle))
    ).normalize()

    height_map_image = Image.open(
        'C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\maps\\5000000000.hght.png')
    height_map_image = height_map_image.convert('RGB')
    height_map_image_width, height_map_image_height = height_map_image.size

    shadow_map = Image.new('RGBA', (height_map_image_width, height_map_image_height), (0x00, 0x00, 0x00, 0x00))
    height_map = [[0 for x in range(height_map_image_width)] for z in range(height_map_image_height)]

    progress_this_time = time()
    delta_time = 0
    display_progress_timeout = 0.5

    for z in range(0, height_map_image_height):
        for x in range(0, height_map_image_width):
            height_map[x][z] = get_height(height_map_image, x, z)

    print("Progress: 0.00%")
    for z in range(0, height_map_image_height):
        for x in range(0, height_map_image_width):
            current_pos = Vector3(x, height_map[x][z], z)
            current_pos_int = (-1, -1)
            last_pos_int = (0, 0)
            print(current_pos, current_pos_int)

            while (
                    0 <= current_pos.x < float(height_map_image_width) and
                    0 <= current_pos.z < float(height_map_image_height) and
                    0 <= current_pos.y < 0xffff
            ):
                progress_last_time = progress_this_time
                progress_this_time = time()
                delta_time += progress_this_time - progress_last_time

                if delta_time >= display_progress_timeout:
                    progress = round(
                        (z * height_map_image_height + x) / (height_map_image_height * height_map_image_width) * 100, 3)
                    print("Progress: {0}%".format(progress))
                    delta_time = 0

                print(current_pos)
                current_pos += sun
                print(current_pos)
                last_pos_int = current_pos_int
                current_pos_int = (int(round(current_pos.x)), int(round(current_pos.z)))
                print(height_map[current_pos_int[0]][current_pos_int[1]])

                if 0 >= current_pos_int[0] > height_map_image_width:
                    print("outside map in x-coord")
                    break

                if 0 >= current_pos_int[1] > height_map_image_height:
                    print("outside map in z-coord")
                    break

                # if math.sqrt((current_pos_int[0] - x) * (current_pos_int[0] - x) + (current_pos_int[1] - z) * (
                #             current_pos_int[1] - z)) > shadow_decay_length:
                #     break

                if last_pos_int[0] == current_pos_int[0] and last_pos_int[1] == current_pos_int[1]:
                    continue

                if current_pos.y <= height_map[current_pos_int[0]][current_pos_int[1]]:
                    print('{0}, {1} is above current pixel'.format(current_pos_int[0], current_pos_int[1]))
                    alpha_pos = math.sqrt(
                        (current_pos_int[0] - x) * (current_pos_int[0] - x) + (current_pos_int[1] - z) * (
                                current_pos_int[1] - z)) / shadow_decay_length
                    alpha = -alpha_pos ** 3 + 1
                    shadow_map.putpixel((x, z), (0x00, 0x00, 0x00, int(alpha * 0xff)))
        exit(1)

    print("Progress: 100.00%")

    print("Saving shadow map...")
    shadow_map.save(
        'C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\maps\\5000000000.shadow.png')

    sys.exit(1)


def get_height(heightMap, x, y):
    r, g, b = heightMap.getpixel((x, y))
    return r << 8 | g << 4 | b & 0xffffff


if __name__ == "__main__":
    main()
