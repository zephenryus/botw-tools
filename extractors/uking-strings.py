import argparse
import codecs

import os
import re
import struct


def get_strings(path):
    print("Extracting Strings from U-King.elf...")

    filename = os.path.basename(path)
    dir = os.path.dirname(os.path.abspath(path))
    extension = os.path.splitext(path)[1]

    if extension != '.elf':
        print("Invalid file extension. Expected '.elf' but saw '{0}'".format(extension))
        return ''

    file = open(path, 'rb')
    print("Reading {0}...".format(filename))

    if file.read(0x04) != b'\x7fELF':
        print("Invalid file format. {0} is not an elf file.".format(filename))

    file.seek(0x10, 0)
    e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = \
        struct.unpack(">HHIIIIIHHHHHH", file.read(0x24))

    print(e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum,
          hex(e_shentsize),
          hex(e_shnum), hex(e_shstrndx))

    section_types = {
        0x0: 'SHT_NULL',
        0x1: 'SHT_PROGBITS',
        0x2: 'SHT_SYMTAB',
        0x3: 'SHT_STRTAB',
        0x4: 'SHT_RELA',
        0x5: 'SHT_HASH',
        0x6: 'SHT_DYNAMIC',
        0x7: 'SHT_NOTE',
        0x8: 'SHT_NOBITS',
        0x9: 'SHT_REL',
        0xa: 'SHT_SHLIB',
        0xb: 'SHT_DYNSYM',
        0xe: 'SHT_INIT_ARRAY',
        0xf: 'SHT_FINI_ARRAY',
        0x10: 'SHT_PREINIT_ARRAY',
        0x11: 'SHT_GROUP',
        0x12: 'SHT_SYMTAB_SHNDX',
        0x60000000: 'SHT_LOOS',
        0x6fffffff: 'SHT_HIOS',
        0x70000000: 'SHT_LOPROC',
        0x7fffffff: 'SHT_HIPROC',
        0x80000000: 'SHT_LOUSER',
        0xffffffff: 'SHT_HIUSER'
    }

    section_header_flags = {
        0x1: 'SHF_WRITE',
        0x2: 'SHF_ALLOC',
        0x4: 'SHF_EXECINSTR',
        0x10: 'SHF_MERGE',
        0x20: 'SHF_STRINGS',
        0x40: 'SHF_INFO_LINK',
        0x80: 'SHF_LINK_ORDER',
        0x100: 'SHF_OS_NONCONFORMING',
        0x200: 'SHF_GROUP',
        0x400: 'SHF_TLS',
        0x0ff00000: 'SHF_MASKOS',
        0xf0000000: 'SHF_MASKPROC'
    }

    # Get string table offset
    file.seek(e_shoff + e_shstrndx * e_shentsize)
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = \
        struct.unpack(">IIIIIIIIII", file.read(e_shentsize))
    string_table_offset = sh_offset

    # Go to section header table
    file.seek(e_shoff, 0)

    section_headers = []

    print("Searching for .rodata...")
    for section_header_index in range(0, e_shnum):
        sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = \
            struct.unpack(">IIIIIIIIII", file.read(e_shentsize))
        section_header = {
            "sh_name": sh_name,
            "sh_type": section_types[sh_type] if sh_type in section_types else 0,
            "sh_flags": section_header_flags[sh_flags] if sh_flags in section_header_flags else 0,
            "sh_addr": sh_addr,
            "sh_offset": sh_offset,
            "sh_size": sh_size,
            "sh_link": sh_link,
            "sh_info": sh_info,
            "sh_addralign": sh_addralign,
            "sh_entsize": sh_entsize
        }

        pos = file.tell()
        file.seek(string_table_offset + sh_name)
        section_header["sh_name"] = file.read().split(b'\x00', 1)[0]
        file.seek(pos)

        if section_header["sh_name"] == b'.rodata':
            rodata_header = section_header = {
                "name": sh_name,
                "type": section_types[sh_type] if sh_type in section_types else 0,
                "flags": section_header_flags[sh_flags] if sh_flags in section_header_flags else 0,
                "addr": sh_addr,
                "offset": sh_offset,
                "size": sh_size,
                "link": sh_link,
                "info": sh_info,
                "addralign": sh_addralign,
                "entsize": sh_entsize
            }
            break

    try:
        rodata_header
    except NameError:
        print('.rodata could not be found. Try running readelf on {0}'.format(filename))
    else:
        print('Reading .rodata...')
        file.seek(rodata_header['offset'])
        data = file.read(rodata_header['size'])
        null_pattern = re.compile(b'([\x00-\x1f]+)')

        print('Extracting strings...')
        strings = re.sub(null_pattern, b'\x0a', data)

        strings_file = codecs.open(dir + '/strings.txt', 'w', 'utf-8')
        strings_file.write(strings.decode('utf-8', 'ignore'))
        strings_file.close()

    file.close()

def main():
    parser = argparse.ArgumentParser(description="The Legend of Zelda: Breath of the Wild U-King.elf String Extractor")
    parser.add_argument("filename", type=str, help="File to be parsed.")
    args = parser.parse_args()

    get_strings(args.filename)

    exit(1)


if __name__ == "__main__":
    main()
