file = "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\5000000000.water.extm\\5000000000.water.extm"

with open(file, 'rb+') as file:
    for index in range(0, 4096):
        file.write(b'\x00\x80')
        file.seek(0x06, 1)

exit(1)