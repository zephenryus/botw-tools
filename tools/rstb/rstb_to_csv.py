import struct
import binascii

data = open("C:\\botw-data\\decompressed\\content\\System\\Resource\\ResourceSizeTable.product.rsizetable", "rb")
csv = open("resource-table.csv", "w")

magic = data.read(4)
assert (magic == b"RSTB")  # Resource Size TaBle?

num_entries, num_extras = struct.unpack(">II", data.read(8))

table = {}

for hash_key, length in struct.iter_unpack(">II", data.read(num_entries * 8)):
    assert (hash_key not in table)  # sanity check
    table[hash_key] = length
    csv.write("{0}, {1}\n".format(hash_key, length))

extras = {}

for _ in range(num_extras):
    filename = data.read(128).rstrip(b"\0")
    file_length = struct.unpack(">I", data.read(4))[0]
    extras[filename] = file_length


def lookup(filename):
    if filename in extras:
        return extras[filename]
    hash_key = binascii.crc32(filename)
    return table[hash_key]


print(lookup(b"Model/DgnMrgPrt_Dungeon000.bfres"))

# for key in extras.keys():
#	print(binascii.crc32(key))
