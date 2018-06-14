import struct


class BFRESNode:
    ref = 0
    left_index = 0
    right_index = 0
    name_offset = 0
    data_offset = 0
    name = ''

    unpack_size = 0x10
    unpack_string = '>i2H2I'

    __node_address: int

    def __init__(self, data, address=0):
        self.__node_address = address
        self.ref = data[0]
        self.left_index = data[1]
        self.right_index = data[2]
        self.name_offset = data[3]
        self.data_offset = data[4]

    def get_node_name(self, infile, rewind=True):
        # The root node has 0 as the name_offset
        if self.ref == -1:
            return 'root'

        pointer = infile.tell()

        infile.seek(self.__node_address + self.name_offset + 0x4)

        string_length = struct.unpack('>I', infile.read(0x04))[0]
        name = infile.read(string_length).decode('utf-8')

        if rewind:
            infile.seek(pointer)

        return name

    def __str__(self):
        return "<BFRESNode> {{\n\tref: {0},\n\tleft_index: {1},\n\tright_index: {2},\n\tname_index: {3},\n\tdata_offset: {4},\n\tname: \"{5}\"\n}}"\
            .format(
                self.ref,
                self.left_index,
                self.right_index,
                hex(self.name_offset),
                hex(self.data_offset),
                self.name
            )

    @staticmethod
    def from_file(infile, offset, rewind=False):
        pointer = infile.tell()
        infile.seek(offset)

        data = BFRESNode(struct.unpack(BFRESNode.unpack_string, infile.read(BFRESNode.unpack_size)), offset)
        data.name = data.get_node_name(infile)

        if rewind:
            infile.seek(pointer)

        return data