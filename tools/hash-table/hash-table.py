import codecs
import json
import struct
from zlib import crc32


def main():
    with open('strings.txt', 'r', encoding='utf8') as file:
        content = file.readlines()
        content = [x.strip() for x in content]

    hashtable = {}
    file = codecs.open('hash-table.json', 'w', 'utf8')
    file.write("{\n")

    for index in range(0, len(content)):
        hash = crc32(bytes(content[index], 'utf8'))
        hashtable[hash] = content[index]

        hexBE = struct.pack('>I', hash)
        hexLE = struct.pack('<I', hash)
        sint = struct.unpack('>i', hexBE)[0]

        file.write(u'\t"{0}": {{ \"string\": {1}, \"uint\": {2}, \"sint\": {3}, \"big-endian\": \"{4}\", \"little-endian\": \"{5}\" }},\n'.format(
            hash,
            json.dumps(content[index]),
            hash,
            sint,
            hexBE.hex(),
            hexLE.hex()
        ))

    file.write("}\n")


if __name__ == "__main__":
    main()
