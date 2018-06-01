import argparse
import os
import struct


def get_data_offset_table(infile, data_offset_table_offset, max_size):
    # store current file position to restore
    current_pointer = infile.tell()
    infile.seek(data_offset_table_offset)

    offsets = []

    # read offset table into array
    while infile.tell() < max_size:
        offset = struct.unpack('>i', infile.read(4))[0]
        if offset >= 0:
            offsets.append(offset)
        else:
            break

    # restore previous file position
    infile.seek(current_pointer)
    return offsets


def save_nav_mesh(infile, filename, data_segment_offset, data_offset_table):
    # store current file position to restore
    current_pointer = infile.tell()

    # +4 because all array lengths start with 00 00 00 00 for some reason
    try:
        infile.seek(data_segment_offset + data_offset_table[16] + 0x4)
    except IndexError:
        return
    face_array_length = struct.unpack('>I', infile.read(0x4))[0]

    infile.seek(data_segment_offset + data_offset_table[18] + 0x4)
    vertex_array_length = struct.unpack('>I', infile.read(0x4))[0]

    face_array = []
    vertex_array = []

    infile.seek(data_segment_offset + data_offset_table[17])
    for _ in range(face_array_length):
        face_array.append(struct.unpack('>iiiii', infile.read(0x14)))

    infile.seek(data_segment_offset + data_offset_table[19])
    for _ in range(vertex_array_length):
        vertex_array.append(struct.unpack('>ffff', infile.read(0x10)))

    print('Exporting {0} to NavMesh/{1}.obj...'.format(filename, filename))

    with open('NavMesh/' + filename + '.obj', 'w') as obj_file:
        obj_file.write('o  {0}\n\n'.format(filename))

        for vertex in vertex_array:
            obj_file.write('v  {0} {1} {2}\n'.format(vertex[0], vertex[1], vertex[2]))

        obj_file.write('\n\nf  ')

        current_vertex = -1
        for face in face_array:
            if current_vertex == -1:
                current_vertex = face[0]
                obj_file.write('\nf  ')
            if face[1] == current_vertex:
                current_vertex = -1
            obj_file.write('{0} '.format(face[0] + 1))


def get_section(infile, data_segment_offset, data_offset_table, section_index, unpack_string, unpack_size):
    # store current file position to restore
    current_pointer = infile.tell()

    # +4 because all array lengths start with 00 00 00 00 for some reason
    try:
        infile.seek(data_segment_offset + data_offset_table[section_index] + 0x4)
    except IndexError:
        return
    array_length = struct.unpack('>I', infile.read(0x4))[0]

    infile.seek(data_segment_offset + data_offset_table[section_index + 1])

    with open('outfile.txt', 'w') as outfile:
        for _ in range(array_length):
            array_entry = struct.unpack('>' + unpack_string, infile.read(unpack_size))

            for val in array_entry:
                outfile.write('{0}\t'.format(val))

            outfile.write('\n')

    infile.seek(current_pointer)


def HKNM2(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            # with open(dirpath + filename, 'rb') as infile:
            with open("C:\\botw-data\\decompressed\\content\\NavMesh\\MainField\\1-1.hknm2", 'rb') as infile:
                if struct.unpack('>q', infile.read(8))[0] == 6332307740630761488:
                    infile.seek(0xe4)  # Beginning of data segment header
                    data_segment_offset, data_offset_table_offset, unk_array_offset0, unk_array_offset0, data_size \
                        = struct.unpack('>IIIII', infile.read(0x14))

                    data_offset_table = get_data_offset_table(infile,
                                                              data_segment_offset + data_offset_table_offset,
                                                              data_segment_offset + unk_array_offset0)

                    # save_nav_mesh(infile, filename, data_segment_offset, data_offset_table)

                    get_section(infile, data_segment_offset, data_offset_table, 28, 'iiii', 16)
            exit()


def main():
    parser = argparse.ArgumentParser(
        description='The Legend of Zelda: Breath of the Wild Havok NavMesh Parser')
    # parser.add_argument("filename", type=str, help="File to be parsed.")
    args = parser.parse_args()

    dirname = "C:\\botw-data\\decompressed\\content\\NavMesh\\MainField\\"

    HKNM2(dirname)


if __name__ == "__main__":
    main()
