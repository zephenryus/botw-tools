import sys
from PIL import Image

terrainHeightMapGradient = [
    [0.00, 0x00, 0x9a, 0x24],
    [0.45, 0xff, 0xff, 0x00],
    [0.90, 0xff, 0x00, 0x00],
    [1.00, 0xff, 0xa0, 0xa0]
]

# terrainHeightMapGradient = [
#     [0.00, 0x00, 0x00, 0x00],
#     [1.00, 0xff, 0xff, 0xff]
# ]

# 405258
# 344044
waterDepthMapGradient = [
    [0.00, 0x15, 0x54, 0xd1],
    [1.00, 0x34, 0x40, 0x44]
]

grassMapGradient = [
    [0.00, 0x00, 0x00, 0x00],
    [1.00, 0xff, 0x00, 0xff]
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


def lerpRGB(colorRangeData, t):
    t = t / colorRangeData[1][0]
    return (
        (int(colorRangeData[0][1] + (colorRangeData[1][1] - colorRangeData[0][1]) * t)),
        (int(colorRangeData[0][2] + (colorRangeData[1][2] - colorRangeData[0][2]) * t)),
        (int(colorRangeData[0][3] + (colorRangeData[1][3] - colorRangeData[0][3]) * t))
    )


def getHeightColor(height, gradient):
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


class HGHT():
    def __init__(self, terrainData, waterData, grassData, mateData):
        print("Extracting HGHT...")

        size = 0x100

        terrain = open(terrainData, 'rb')
        water = open(waterData, 'rb')
        grass = open(grassData, 'rb')
        mate = open(mateData, 'rb')

        heightMap = [any] * size * size
        heightMapImage = Image.new("RGB", (size, size))
        heightMax = 0xffff

        pos = 0

        # Build terrain height map
        for y in range(0, int(size / 1)):
            for x in range(0, int(size / 1)):
                height = int.from_bytes(terrain.read(2), 'little')
                heightMap[y * size + x] = height / heightMax
                color = lerpRGB(getHeightColor(height / heightMax, terrainHeightMapGradient), height / heightMax)
                heightMapImage.putpixel((x, y), color)

        # Build water height map
        for y in range(0, int(size / 4)):
            for x in range(0, int(size / 4)):
                height = int.from_bytes(water.read(2), 'little')
                water.read(6)

                for y2 in range(0, 4):
                    for x2 in range(0, 4):
                        if height / heightMax > heightMap[(y * 4 + y2) * size + x * 4 + x2]:
                            color = lerpRGB(
                                getHeightColor(
                                    height / heightMax - heightMap[(y * 4 + y2) * size + x * 4 + x2],
                                    waterDepthMapGradient
                                ),
                                height / heightMax - heightMap[(y * 4 + y2) * size + x * 4 + x2]
                            )
                            heightMapImage.putpixel((x * 4 + x2, y * 4 + y2), color)

        # Build grass height map
        # for y in range(0, int(size / 8)):
        #     for x in range(0, int(size / 8)):
        #         height = int.from_bytes(grass.read(2), 'little')
        #         grass.read(2)
        #
        #         for y2 in range(0, 8):
        #             for x2 in range(0, 8):
        #                 if height / heightMax > heightMap[(y * 8 + y2) * size + x * 8 + x2]:
        #                     color = lerpRGB(
        #                         getHeightColor(
        #                             height / heightMax - heightMap[(y * 8 + y2) * size + x * 8 + x2],
        #                             grassMapGradient
        #                         ),
        #                         height / heightMax - heightMap[(y * 8 + y2) * size + x * 8 + x2],
        #                     )
        #
        #                     heightMapImage.putpixel((x * 8 + x2, y * 8 + y2), color)

        # Build mate height map
        # for y in range(0, int(size / 1)):
        #     for x in range(0, int(size / 1)):
        #         height = int.from_bytes(mate.read(2), 'little')
        #         mate.read(2)
        #         heightMap[y * size + x] = height / heightMax
        #         color = lerpRGB(getHeightColor(height / heightMax, mateMapGradient),
        #                         height / heightMax)
        #         heightMapImage.putpixel((x, y), color)

        print("Saving height map...")
        heightMapImage.save("C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\5000000000.png")
        pass


def main():
    print("HGHTExtract by zephenryus")

    # if len(sys.argv) != 2:
    #     print("Usage: <inputFile>")
    #     sys.exit(1)

    # with open(sys.argv[1], "rb") as hghtFile:

    HGHT(
        "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\5000000000.hght",
        "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\5000000000.water.extm",
        "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\5000000000.grass.extm",
        "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000\\5000000000.mate",
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
