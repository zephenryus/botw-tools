import argparse

import os
import struct


class FRES:
    offsets = {
        'name': 0,
        'string_table': 0,
        'model_list': 0,
        'texture_list': 0,
        'skeletal_anim_list': 0,
        'shader_param_anim_list': 0,
        'color_anim_list': 0,
        'tex_srt_anim_list': 0,
        'tex_pattern_anim_list': 0,
        'bone_vis_anim_list': 0,
        'mat_vis_anim_list': 0,
        'shape_anim_list': 0,
        'scene_anim_list': 0,
        'external_file_list': 0
    }

    def __init__(self, path):
        print("Parsing Binary Terrain Scene file...")

        filename = os.path.basename(path)
        print("Reading {0}...".format(filename))

        file = open(path, 'rb')
        self.data = file.read()

        signature = self.data[0x00:0x04]
        byte_order = self.data[0x08:0x0a]

        if signature != b'FRES':
            print('\033[31mQuitting: {0} is not a BFRES file\033[0m'.format(filename))
            print('\033[31mExpected b\'FRES\' but saw {0}\033[0m'.format(signature))
            exit(0)

        bom = '<'
        if byte_order == b'\xfe\xff':
            bom = '>'

        version = struct.unpack(bom + 'BBBB', self.data[0x04:0x08])
        header_size, file_size, align = struct.unpack(bom + 'HII', self.data[0x0a:0x14])

        pos = 0x14

        name_offset = struct.unpack(bom + 'I', self.data[pos:pos + 0x04])[0] + pos
        name = self.data[name_offset:].split(b'\x00', 1)[0].decode('utf-8', 'strict')

        pos += 0x04
        string_table_size, string_table_offset = struct.unpack(bom + 'II', self.data[pos:pos + 0x08])
        pos += 0x04
        string_table_offset += pos

        # , string_table_size, string_table_offset, model_table_offset, texture, skeletal_anim, shader_anim, shader_param_anim, tex_srt_anim, tex_pattern_anim, bone_vis_anim, mat_vis_anim, shape_anim, scene_anim, external_file, model_count, texture_count, skeletal_anim_count, shader_param_anim_count
        print(hex(name_offset), name, string_table_size, hex(string_table_offset))


def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild bfres parser")
    parser.add_argument("filename", type=str, help="File to be parsed.")

    args = parser.parse_args()

    bfres = FRES(args.filename)


if __name__ == "__main__":
    main()
