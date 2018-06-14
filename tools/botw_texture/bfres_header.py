import struct

from src.tools.botw_texture.bfres_header_count_table import BFRESHeaderCountTable
from src.tools.botw_texture.bfres_header_offset_table import BFRESHeaderOffsetTable


class BFRESHeader:
    signature = b''
    bfres_version = 0
    byte_order = 0
    header_size = 0
    file_size = 0
    alignment = 0
    filename_offset = 0
    string_pool_size = 0
    offset_table: BFRESHeaderOffsetTable
    count_table = {}
    filename = ''

    unpack_size = 0x68
    unpack_string = '>4sI2H17I12H'

    def __init__(self, data):
        self.signature = data[0]
        self.bfres_version = data[1]
        self.byte_order = data[2]
        self.header_size = data[3]
        self.file_size = data[4]
        self.alignment = data[5]
        self.filename_offset = data[6]
        self.string_pool_size = data[7]
        self.offset_table = BFRESHeaderOffsetTable(data[8], data[9], data[10], data[11], data[12], data[13], data[14],
                                                   data[15], data[16], data[17], data[18], data[19], data[20])
        self.count_table = BFRESHeaderCountTable(data[21], data[22], data[23], data[24], data[25], data[26], data[27],
                                                 data[28], data[29], data[30], data[31])

    def get_filename(self, infile, rewind=True):
        pointer = infile.tell()
        infile.seek(self.header_size + self.filename_offset)

        filename_string_length = struct.unpack('>I', infile.read(0x04))[0]
        filename = infile.read(filename_string_length).decode('utf-8')

        if rewind:
            infile.seek(pointer)

        return filename

    def __str__(self):
        return "<BFRESHeader> {{\n\tsignature: {0},\n\tbfres_version: {1},\n\tbyte_order: {2},\n\theader_size: {3},\n\t" \
               "file_size: {4},\n\talignment: {5},\n\tfilename_offset: {6},\n\tstring_pool_size: {7},\n\toffset_table: {8},\n\t" \
               "count_table: {9},\n\tfilename: \"{10}\"\n}}" \
            .format(
            self.signature,
            self.bfres_version,
            self.byte_order,
            self.header_size,
            self.file_size,
            self.alignment,
            self.filename_offset,
            self.string_pool_size,
            self.offset_table,
            self.count_table,
            self.filename
        )

    @staticmethod
    def from_file(infile, rewind=False):
        pointer = infile.tell()
        infile.seek(0)

        data = BFRESHeader(struct.unpack(BFRESHeader.unpack_string, infile.read(BFRESHeader.unpack_size)))
        data.filename = data.get_filename(infile)

        if rewind:
            infile.seek(pointer)

        return data
