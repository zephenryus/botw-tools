import argparse
import sys
import os
from PIL import Image

terrainHeightMapGradient = [
    [0.00, 0x00, 0x9a, 0x24],
    [0.45, 0xff, 0xff, 0x00],
    [0.90, 0xff, 0x00, 0x00],
    [1.00, 0xff, 0xa0, 0xa0]
]

waterHeightMapGradient = [
    [0.00, 0x34, 0x40, 0x44],
    [1.00, 0x15, 0x54, 0xd1]
]

waterDepthMapGradient = [
    [0.00, 0x15, 0x54, 0xd1],
    [1.00, 0x34, 0x40, 0x44]
]

grassMapGradient = [
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

mateMapGradient = [
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

grayScaleGradient = [
    [0.00, 0x00, 0x00, 0x00],
    [1.00, 0xff, 0xff, 0xff]
]


class HGHT():
    def __init__(self, path, isTerrain, isWater, isMaterial, isGrass, isComposite, isGrayScale):
        print("Extracting HGHT...")

        fileName = os.path.splitext(path)[0]
        size = 0x100

        if isGrayScale:
            terrainHeightMapGradient = grayScaleGradient
            waterHeightMapGradient = grayScaleGradient
            grassMapGradient = grayScaleGradient
            mateMapGradient = grayScaleGradient

        if isTerrain:
            if os.path.isfile(fileName + ".hght"):
                self.createMap(fileName, ".hght", size, terrainHeightMapGradient, 0, 1)
            else:
                print("\033[93mSkipping " + fileName + ".hght because it does not exist\033[0m")

        if isWater:
            if os.path.isfile(fileName + ".water.extm"):
                self.createMap(fileName, ".water.extm", size, waterHeightMapGradient, 6, 4)
            else:
                print("\033[93mSkipping " + fileName + ".water.extm because it does not exist\033[0m")

        if isGrass:
            if os.path.isfile(fileName + ".grass.extm"):
                self.createMap(fileName, ".grass.extm", size, grassMapGradient, 2, 4)
            else:
                print("\033[93mSkipping " + fileName + ".grass.extm because it does not exist\033[0m")

        if isMaterial:
            if os.path.isfile(fileName + ".mate"):
                self.createMap(fileName, ".mate", size, mateMapGradient, 2, 1)
            else:
                print("\033[93mSkipping " + fileName + ".mate because it does not exist\033[0m")

        if isComposite:
            if os.path.isfile(fileName + ".hght") and os.path.isfile(fileName + ".water.extm"):
                self.createCompositeMap(fileName, terrainHeightMapGradient, waterDepthMapGradient)
            else:
                print("\033[93mSkipping composite because .hght or .water.extm do not exist\033[0m")

        return

    def createMap(self, fileName, extension=".hght", size=0x100, gradient=None, padding=0, blockSize=1):
        if gradient is None:
            gradient = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        data = open(fileName + extension, 'rb')
        print("Reading " + os.path.basename(fileName) + extension + " data...")

        map = self.getHeightMap(data, 0xffff, size, padding, blockSize)
        print("Creating " + os.path.basename(fileName) + extension + " map...")

        mapImage = self.getHeightMapImage(map, 0xffff, size, gradient, blockSize)
        print("Saving " + os.path.basename(fileName) + extension + ".png...")
        mapImage.save(fileName + extension + ".png")

    def getHeightMap(self, data, heightMax=0xffff, size=0x100, padding=0, blockSize=1):
        heightMap = [any] * size * size

        for y in range(0, int(size / blockSize)):
            for x in range(0, int(size / blockSize)):
                height = int.from_bytes(data.read(2), 'little')
                data.read(padding)

                for y2 in range(0, blockSize):
                    for x2 in range(0, blockSize):
                        heightMap[(y * blockSize + y2) * size + x * blockSize + x2] = height / heightMax

        return heightMap

    def getHeightMapImage(self, heightMap, heightMax=0xffff, size=0x100, colorGradient=None, blockSize=1):
        heightMapImage = Image.new("RGB", (size, size))

        if colorGradient == None:
            colorGradient = [
                [0.00, 0x00, 0x00, 0x00],
                [1.00, 0xff, 0xff, 0xff]
            ]

        for y in range(0, size):
            for x in range(0, size):
                height = heightMap[y * size + x]

                color = self.lerpRGB(self.getHeightColor(height, colorGradient), height)
                heightMapImage.putpixel((x, y), color)

        return heightMapImage

    def createCompositeMap(self, fileName, terrainGradient, waterGradient):
        size = 0x100
        compositeMapImage = Image.new("RGB", (size, size))

        print("Reading composite data...")
        terrain = open(fileName + '.hght', 'rb')
        water = open(fileName + '.water.extm', 'rb')

        print("Creating composite map...")
        terrainHeightMap = self.getHeightMap(terrain, 0xffff, size, 0, 1)
        waterHeightMap = self.getHeightMap(water, 0xffff, size, 6, 4)

        for y in range(0, size):
            for x in range(0, size):
                terrainHeight = terrainHeightMap[y * size + x]
                waterHeight = waterHeightMap[y * size + x]

                if (waterHeight > terrainHeight):
                    depth = waterHeight - terrainHeight
                    color = self.lerpRGB(self.getHeightColor(depth, waterGradient), depth)
                else:
                    color = self.lerpRGB(self.getHeightColor(terrainHeight, terrainGradient), terrainHeight)
                compositeMapImage.putpixel((x, y), color)

        print("Saving " + os.path.basename(fileName) + ".composite.png...")
        compositeMapImage.save(fileName + ".composite.png")

    def lerpRGB(self, colorRangeData, t):
        t = t / colorRangeData[1][0]
        return (
            (int(colorRangeData[0][1] + (colorRangeData[1][1] - colorRangeData[0][1]) * t)),
            (int(colorRangeData[0][2] + (colorRangeData[1][2] - colorRangeData[0][2]) * t)),
            (int(colorRangeData[0][3] + (colorRangeData[1][3] - colorRangeData[0][3]) * t))
        )

    def getHeightColor(self, height, gradient):
        currentHeight = 0.0
        currentColor = (0, 0, 0, 0)
        lastHeight = 0.0
        lastColor = (0, 0, 0, 0)

        for index in range(0, len(gradient)):
            lastHeight = currentHeight
            lastColor = currentColor
            currentHeight = gradient[index][0]
            currentColor = (
                currentHeight,
                gradient[index][1],
                gradient[index][2],
                gradient[index][3],
            )

            if height < gradient[index][0]:
                break

        return (lastColor, currentColor)


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
    parser.add_argument("--grayscale",
                        help="Generate as gray scale map",
                        action="store_true")
    args = parser.parse_args()

    imageTypes = (False, False, False, False, False, False)

    if args.terrain:
        imageTypes = (True, imageTypes[1], imageTypes[2], imageTypes[3], imageTypes[4], imageTypes[5])

    if args.water:
        imageTypes = (imageTypes[0], True, imageTypes[2], imageTypes[3], imageTypes[4], imageTypes[5])

    if args.material:
        imageTypes = (imageTypes[0], imageTypes[1], True, imageTypes[3], imageTypes[4], imageTypes[5])

    if args.grass:
        imageTypes = (imageTypes[0], imageTypes[1], imageTypes[2], True, imageTypes[4], imageTypes[5])

    if args.composite:
        imageTypes = (imageTypes[0], imageTypes[1], imageTypes[2], imageTypes[3], True, imageTypes[5])

    if args.grayscale:
        print("is grayscale")
        imageTypes = (imageTypes[0], imageTypes[1], imageTypes[2], imageTypes[3], imageTypes[4], True)

    if args.all:
        imageTypes = (True, True, True, True, True, imageTypes[5])

    if not args.all and not args.terrain and not args.water and not args.material and not args.grass \
            and not args.composite:
        imageTypes = (True, True, True, True, True, imageTypes[5])

    HGHT(args.filename, imageTypes[0], imageTypes[1], imageTypes[2], imageTypes[3], imageTypes[4], imageTypes[5])

    sys.exit(1)


if __name__ == "__main__":
    main()
