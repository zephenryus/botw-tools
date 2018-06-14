import struct


class FGX2Surface:
    texture_type = 0
    width = 0
    height = 0
    depth = 0
    mip_map_count = 0
    texture_format = 0
    anti_aliasing_mode = 0
    texture_usage = 0
    texture_data_size = 0
    runtime_data_pointer = 0
    mip_map_data_size = 0
    runtime_mip_map_data_pointer = 0
    tile_mode = 0
    swizzle = 0
    alignment = 0
    pitch = 0

    unpack_size = 0x40
    unpack_string = '>16I'

    def __init__(self, data):
        self.texture_type = data[0]
        self.width = data[1]
        self.height = data[2]
        self.depth = data[3]
        self.mip_map_count = data[4]
        self.texture_format = data[5]
        self.anti_aliasing_mode = data[6]
        self.texture_usage = data[7]
        self.texture_data_size = data[8]
        self.runtime_data_pointer = data[9]
        self.mip_map_data_size = data[10]
        self.runtime_mip_map_data_pointer = data[11]
        self.tile_mode = data[12]
        self.swizzle = data[13]
        self.alignment = data[14]
        self.pitch = data[15]

    def __str__(self):
        return "<FGX2Surface> {{\n\ttexture_type: {0},\n\twidth: {1},\n\theight: {2},\n\tdepth: {3},\n\tmip_map_count: {4},\n\ttexture_format: {5},\n\tanti_aliasing_mode: {6},\n\ttexture_usage: {7},\n\ttexture_data_size: {8},\n\truntime_data_pointer: {9},\n\tmip_map_data_size: {10},\n\truntime_mip_map_data_pointer: {11},\n\ttile_mode: {12},\n\tswizzle: {13},\n\talignment: {14},\n\tpitch: {15}\n}}\n".format(
            self.texture_type,
            self.width,
            self.height,
            self.depth,
            self.mip_map_count,
            self.texture_format,
            self.anti_aliasing_mode,
            self.texture_usage,
            self.texture_data_size,
            self.runtime_data_pointer,
            self.mip_map_data_size,
            self.runtime_mip_map_data_pointer,
            self.tile_mode,
            self.swizzle,
            self.alignment,
            self.pitch
        )

    @staticmethod
    def from_file(infile, rewind=False):
        pointer = infile.tell()

        data = FGX2Surface(struct.unpack(FGX2Surface.unpack_string, infile.read(FGX2Surface.unpack_size)))

        if rewind:
            infile.seek(pointer)

        return data