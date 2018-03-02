import struct

with open('C:\\botw-data\\decompressed\\content\\Model\\Obj_MashroomHeart_A.bfres', 'rb') as file:
    magic = file.read(4) # read 4 bytes

    if magic != b'FRES':
        print('This does not appear to be a valid bfres file')
        exit(0)

    version_0, version_1, version_2, version_3, bom, header_length, file_length, file_alignment, \
        file_name_offset, string_table_length, string_table_offset \
        = struct.unpack('>BBBBHHIIIII', file.read(28))

    print(version_0, version_1, version_2, version_3, bom, header_length, file_length, file_alignment, file_name_offset, string_table_length, string_table_offset)
