import ctypes
import os
import struct
import tempfile

from shutil import copyfile


class Yaz0:
    @staticmethod
    def decompress(path):
        if os.path.exists(path):
            with open(path, 'rb') as file:
                filename = os.path.basename(path)
                base_file, extension = os.path.splitext(filename)
                extension = extension[1:].replace('s', '', 1)
                base_path = os.path.dirname(os.path.realpath(path))
                out_file = base_path + '\\' + base_file + '.' + extension

                print("Decompressing {0}...".format(filename))

                tmp = tempfile.TemporaryFile('w+b')
                tmp.seek(0)

                if file.read(0x04) == b'Yaz0':
                    decompressed_size = struct.unpack('>I8x', file.read(0x0c))[0]

                    group_header = 0
                    valid_bit_count = 0

                    kernel32 = ctypes.windll.kernel32

                    ticks = kernel32.GetTickCount()
                    show_progress_on_tick_count = 1000

                    while tmp.tell() < decompressed_size:
                        #
                        if kernel32.GetTickCount() - ticks > show_progress_on_tick_count:
                            print('{0} / {1}'.format(tmp.tell(), decompressed_size))
                            ticks = kernel32.GetTickCount()

                        if valid_bit_count == 0:
                            group_header = struct.unpack('>B', file.read(0x01))[0]
                            valid_bit_count = 8

                        if (group_header & 0x80) != 0:
                            tmp.write(file.read(0x01))

                        else:
                            b1, b2 = struct.unpack('>BB', file.read(0x02))

                            distance = (b1 & 0xf) << 8 | b2
                            copy_source = tmp.tell() - (distance + 1)
                            num_bytes = b1 >> 4

                            if num_bytes == 0:
                                num_bytes = struct.unpack('>B', file.read(0x01))[0] + 0x12

                            else:
                                num_bytes += 2

                            write_pos = tmp.tell()
                            copy_pos = copy_source

                            for _ in range(num_bytes):
                                tmp.seek(copy_source)
                                copy = tmp.read(0x01)

                                tmp.seek(write_pos)
                                tmp.write(copy)

                                write_pos = tmp.tell()
                                copy_pos += 1

                        group_header <<= 1
                        valid_bit_count -= 1

                    copyfile(tmp.name, out_file)

                else:
                    print("{0} is not a Yaz0 compressed file.")
                    return False

        else:
            print("{0} does not exist.")
            return False
