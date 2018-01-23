import tempfile
import os

temp = tempfile.NamedTemporaryFile(mode='rb+')
filename = "C:\\botw-data\\decompressed\\content\\Terrain\\A\\MainField\\550000025C.water.extm\\550000025E.water.extm"
file = open(filename, 'rb')
size = os.path.getsize(filename)

for index in range(0, int(size / 8)):
    entry = file.read(8)
    temp.write(entry[0:7] + b'\x00')
    # temp.write(b'\xff\xff\x00\x80\x00\x80\x00\x00')

file.close()
temp.seek(0)
file = open(filename, 'wb')

for line in temp:
    file.write(line)

temp.close()