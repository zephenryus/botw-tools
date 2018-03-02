import os

import src.extractors.sarc

with open("C:\\botw-data\\src\\tools\\file-types\yaz0.txt") as yaz_list:
    for yaz_file_name in yaz_list:
        yaz_file = yaz_file_name.rstrip()
        if os.path.exists(yaz_file):
            with open(yaz_file, 'rb') as file:
                data = file.read()

                magic = data[0:4]

                if magic == b"Yaz0":
                    decompressed = src.extractors.sarc.yaz0_decompress(data)
                    if decompressed[0:4] == b'SARC':
                        src.extractors.sarc.sarc_extract(decompressed, 1, yaz_file)
                    else:
                        filename, extension = os.path.splitext(yaz_file)
                        outfile = filename + '.' + extension[1:].replace('s', '', 1)
                        with open(outfile, 'wb') as yaz0:
                            print('Decompressing to {0}'.format(outfile))
                            yaz0.write(decompressed)

                            if os.path.exists(outfile):
                                file.close()
                                os.remove(yaz_file)

                elif magic == b"SARC":
                    src.extractors.sarc.sarc_extract(data, 0, yaz_file)
