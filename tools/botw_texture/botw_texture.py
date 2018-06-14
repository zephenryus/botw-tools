import argparse
import struct
import sys

from src.tools.botw_texture.bfres_header import BFRESHeader
from src.tools.botw_texture.bfres_node import BFRESNode
from src.tools.botw_texture.egx2_surface_dim import EGX2SurfaceDim
from src.tools.botw_texture.egx2_surface_format import EGX2SurfaceFormat
from src.tools.botw_texture.fgx2_surface import FGX2Surface


class AddrTileType:
    ADDR_DISPLAYABLE = 0x0
    ADDR_NON_DISPLAYABLE = 0x1
    ADDR_DEPTH_SAMPLE_ORDER = 0x2
    ADDR_THICK_TILING = 0x3


class AddrTileMode:
    ADDR_TM_LINEAR_GENERAL = 0x0
    ADDR_TM_LINEAR_ALIGNED = 0x1
    ADDR_TM_1D_TILED_THIN1 = 0x2
    ADDR_TM_1D_TILED_THICK = 0x3
    ADDR_TM_2D_TILED_THIN1 = 0x4
    ADDR_TM_2D_TILED_THIN2 = 0x5
    ADDR_TM_2D_TILED_THIN4 = 0x6
    ADDR_TM_2D_TILED_THICK = 0x7
    ADDR_TM_2B_TILED_THIN1 = 0x8
    ADDR_TM_2B_TILED_THIN2 = 0x9
    ADDR_TM_2B_TILED_THIN4 = 0xA
    ADDR_TM_2B_TILED_THICK = 0xB
    ADDR_TM_3D_TILED_THIN1 = 0xC
    ADDR_TM_3D_TILED_THICK = 0xD
    ADDR_TM_3B_TILED_THIN1 = 0xE
    ADDR_TM_3B_TILED_THICK = 0xF
    ADDR_TM_LINEAR_SPECIAL = 0x10
    ADDR_TM_2D_TILED_XTHICK = 0x10
    ADDR_TM_3D_TILED_XTHICK = 0x11
    ADDR_TM_POWER_SAVE = 0x12
    ADDR_TM_COUNT = 0x13


class AddrPipeCfg:
    ADDR_PIPECFG_INVALID = 0x0
    ADDR_PIPECFG_P2 = 0x1
    ADDR_PIPECFG_P4_8x16 = 0x5
    ADDR_PIPECFG_P4_16x16 = 0x6
    ADDR_PIPECFG_P4_16x32 = 0x7
    ADDR_PIPECFG_P4_32x32 = 0x8
    ADDR_PIPECFG_P8_16x16_8x16 = 0x9
    ADDR_PIPECFG_P8_16x32_8x16 = 0xA
    ADDR_PIPECFG_P8_32x32_8x16 = 0xB
    ADDR_PIPECFG_P8_16x32_16x16 = 0xC
    ADDR_PIPECFG_P8_32x32_16x16 = 0xD
    ADDR_PIPECFG_P8_32x32_16x32 = 0xE
    ADDR_PIPECFG_P8_32x64_32x32 = 0xF
    ADDR_PIPECFG_MAX = 0x10


class AddrTileInfo:
    banks: int
    bankWidth: int
    bankHeight: int
    macroAspectRatio: int
    tileSplitBytes: int
    pipeConfig: AddrPipeCfg


class AddrExtractBankPipeSwizzleInput:
    size: int
    base256b: int
    tileInfo: AddrTileInfo
    tileIndex: int


class AddrExtractBankPipeSwizzleOutput:
    size: int
    bankSwizzle: int
    pipeSwizzle: int


class AddrComputeSurfaceAddrFromCoordInput:
    size: int
    x: int
    y: int
    slice: int
    sample: int
    bits_per_pixel: int
    pitch: int
    height: int
    num_slices: int
    num_samples: int
    tile_mode: AddrTileMode
    is_depth: bool
    tile_base: int
    comp_bits: int
    pipe_swizzle: int
    bank_swizzle: int
    num_frags: int
    tile_type: AddrTileType
    ignore_se: bool
    __pad: int
    tile_index: int


class TerrainTexture(object):
    def __init__(self, path):
        with open(path, 'rb') as self.infile:
            header = BFRESHeader.from_file(self.infile)

            if header.signature != b'FRES':
                print('Invalid bfres file')
                exit(101)

            # +0x14 to get to the texture offset value at 0x24
            self.infile.seek(header.header_size + 0x14 + header.offset_table.texture_dictionary)
            size, node_length = struct.unpack('>2I', self.infile.read(0x08))

            nodes = []
            for _ in range(node_length + 1):
                nodes.append(BFRESNode.from_file(self.infile, self.infile.tell()))

            # Read textures
            if self.infile.read(0x04) != b'FTEX':
                print('Invalid texture')
                exit(102)

            fgx2_surface = FGX2Surface.from_file(self.infile)

            mip_offset = gx2_comp_sel = gx2_texture_regs = []
            mip_offset = struct.unpack('>13I', self.infile.read(0x34))
            view_mip_first, view_mip_count, view_slice_first, view_slice_count = struct.unpack('>4I',
                                                                                               self.infile.read(0x10))
            gx2_comp_sel = struct.unpack('>4B', self.infile.read(0x04))
            gx2_texture_regs = struct.unpack('>5I', self.infile.read(0x14))
            handle, array_length = struct.unpack('>Ib3x', self.infile.read(0x08))

            name_offset_offset = self.infile.tell() - 0x04
            name_offset = struct.unpack('>I', self.infile.read(0x04))[0]
            name_offset += name_offset_offset

            path_offset = struct.unpack('>I', self.infile.read(0x04))[0]

            image_data_offset_offset = self.infile.tell()
            image_data_offset = struct.unpack('>I', self.infile.read(0x04))[0]
            image_data_offset += image_data_offset_offset

            mip_data_offset, user_data_dict_offset, user_data_count = struct.unpack('>2Ih2x', self.infile.read(0x0c))

            self.infile.seek(image_data_offset)

            bits_per_pixel = self.get_bits_per_pixel(fgx2_surface.texture_format)

            source_num_blocks_width = fgx2_surface.width
            source_num_blocks_height = fgx2_surface.height
            source_pitch = fgx2_surface.pitch

            upload_width = source_num_blocks_width
            upload_height = source_num_blocks_height
            upload_pitch = source_num_blocks_width
            upload_depth = fgx2_surface.depth

            compressed_formats = [
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC1_UNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC1_SRGB,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC2_UNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC2_SRGB,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC3_UNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC3_SRGB,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC4_UNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC4_SNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC5_UNORM,
                EGX2SurfaceFormat.GX2_SURFACE_FORMAT_T_BC5_SNORM
            ]

            for format in compressed_formats:
                if format == fgx2_surface.texture_format:
                    source_num_blocks_width = (source_num_blocks_width + 3) / 4
                    source_num_blocks_height = (source_num_blocks_height + 3) / 4

                    upload_width = source_num_blocks_width * 4
                    upload_height = source_num_blocks_height * 4
                    upload_pitch = upload_width / 4

                    break

            if fgx2_surface.texture_type == EGX2SurfaceDim.GX2_SURFACE_DIM_CUBE:
                upload_depth *= 6

            source_image_size = (source_num_blocks_width * source_num_blocks_height * upload_depth * bits_per_pixel) / 8
            built_in_source_image_size = fgx2_surface.texture_data_size
            size_match = source_image_size == built_in_source_image_size

            destination_image_size = (
                                             source_num_blocks_width * source_num_blocks_height * upload_depth * bits_per_pixel) / 8
            aligned_destination_image_size = destination_image_size + (
                    fgx2_surface.alignment - (destination_image_size % fgx2_surface.alignment))

            output_buffer = [0xff] * int(aligned_destination_image_size)

            self.convert_from_tiled(output_buffer, upload_pitch, self.infile, fgx2_surface.tile_mode,
                                    fgx2_surface.swizzle, source_pitch, source_num_blocks_width,
                                    source_num_blocks_height, upload_depth, fgx2_surface.anti_aliasing_mode,
                                    bits_per_pixel, False)

    def read_name(self, offset):
        pointer = self.infile.tell()
        self.infile.seek(offset)
        string_length = struct.unpack('>I', self.infile.read(0x04))[0]
        name = self.infile.read(string_length)
        self.infile.seek(pointer)
        return name

    def get_bits_per_pixel(self, format):
        hardware_format_info = [
            0x00, 0x00, 0x00, 0x01, 0x08, 0x03, 0x00, 0x01, 0x08, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x00, 0x00, 0x00, 0x01, 0x10, 0x07, 0x00, 0x00, 0x10, 0x03, 0x00, 0x01, 0x10, 0x03, 0x00, 0x01,
            0x10, 0x0B, 0x00, 0x01, 0x10, 0x01, 0x00, 0x01, 0x10, 0x03, 0x00, 0x01, 0x10, 0x03, 0x00, 0x01,
            0x10, 0x03, 0x00, 0x01, 0x20, 0x03, 0x00, 0x00, 0x20, 0x07, 0x00, 0x00, 0x20, 0x03, 0x00, 0x00,
            0x20, 0x03, 0x00, 0x01, 0x20, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x03, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x20, 0x03, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x00, 0x00, 0x00, 0x01, 0x20, 0x0B, 0x00, 0x01, 0x20, 0x0B, 0x00, 0x01, 0x20, 0x0B, 0x00, 0x01,
            0x40, 0x05, 0x00, 0x00, 0x40, 0x03, 0x00, 0x00, 0x40, 0x03, 0x00, 0x00, 0x40, 0x03, 0x00, 0x00,
            0x40, 0x03, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x80, 0x03, 0x00, 0x00, 0x80, 0x03, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x10, 0x01, 0x00, 0x00,
            0x10, 0x01, 0x00, 0x00, 0x20, 0x01, 0x00, 0x00, 0x20, 0x01, 0x00, 0x00, 0x20, 0x01, 0x00, 0x00,
            0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x60, 0x01, 0x00, 0x00,
            0x60, 0x01, 0x00, 0x00, 0x40, 0x01, 0x00, 0x01, 0x80, 0x01, 0x00, 0x01, 0x80, 0x01, 0x00, 0x01,
            0x40, 0x01, 0x00, 0x01, 0x80, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        hardware_format = format & 0x3f
        return hardware_format_info[hardware_format * 4]

    def convert_from_tiled(self, output, output_pitch, input, tile_mode, swizzle, pitch, width, height, depth,
                           anti_aliasing, bits_per_pixel, is_depth):
        source_addr_input = AddrComputeSurfaceAddrFromCoordInput
        source_addr_input.bits_per_pixel = bits_per_pixel
        source_addr_input.pitch = pitch
        source_addr_input.height = height
        source_addr_input.num_slices = depth
        source_addr_input.num_samples = anti_aliasing
        source_addr_input.is_depth = is_depth
        source_addr_input.tile_base = 0
        source_addr_input.comp_bits = 0
        source_addr_input.num_frags = 0

        source_addr_input.bank_swizzle, source_addr_input.pipe_swizzle = self.calculate_surface_bank_pipe_swizzle(
            swizzle)

    def calculate_surface_bank_pipe_swizzle(self, swizzle):
        input = AddrExtractBankPipeSwizzleInput
        input.size = sys.getsizeof(AddrExtractBankPipeSwizzleInput)

        output = AddrExtractBankPipeSwizzleOutput
        output.size = sys.getsizeof(AddrExtractBankPipeSwizzleOutput)

        input.base256b = (swizzle >> 8) & 0xff
        # input, output = self.addr_extract_bank_pipe_swizzle()

        return (0, 0)


def main():
    parser = argparse.ArgumentParser(
        description='The Legend of Zelda: Breath of the Wild texture extractor')
    # parser.add_argument("filename", type=str, help="Texture file to be extracted.")
    # args = parser.parse_args()

    filename = "C:\\botw-data\\decompressed\\content\\Model\\Terrain.Tex1.bfres"

    TerrainTexture(filename)


if __name__ == "__main__":
    main()
