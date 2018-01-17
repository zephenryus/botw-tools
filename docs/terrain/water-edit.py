import tempfile
import os

temp = tempfile.NamedTemporaryFile(mode='rb+')
file = open("C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\58000096F4.water.extm\\58000096F6.water.extm", 'rb')
size = os.path.getsize("C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\58000096F4.water.extm\\58000096F6.water.extm")

for index in range(0, int(size / 8)):
    entry = file.read(8)
    temp.write(entry[0:7] + b'\x03')

file.close()
temp.seek(0)
file = open("C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\58000096F4.water.extm\\58000096F6.water.extm", 'wb')

for line in temp:
    file.write(line)

temp.close()