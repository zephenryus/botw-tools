import os
import struct
import tempfile


class Yaz0:
    pointer_stack = []

    @staticmethod
    def decode(path: str) -> bytes:
        yaz_file = path.strip()
        if os.path.exists(yaz_file):
            with open(yaz_file, 'rb') as infile:
                # Thanks to thakis for yaz0dec, which I modeled this on after
                # I cleaned it up in v0.2, what with bit-manipulation and looping
                # Thanks to Kinnay for suggestions to make this even faster
                print("Decoding Yaz0....")
                data = infile.read()

                original_size = os.path.getsize(yaz_file)
                pos = 16
                size = struct.unpack('>I', data[pos:pos + 0x04])[0]  # Uncompressed filesize
                out = []
                out_len = 0

                dstpos = 0
                percent = 0
                bits = 0
                code = 0

                if len(data) >= 5242880:
                    count = 5  # 5MB is gonna take a while
                else:
                    count = 10

                while len(out) < size:  # Read Entire File
                    # percent = check(out_len, size, percent, count)

                    if bits == 0:
                        code = struct.unpack('>B', data[pos:pos + 1])[0]
                        pos += 1
                        bits = 8

                    if (code & 0x80) != 0:  # Copy 1 Byte
                        out.append(data[pos])
                        pos += 1
                        out_len += 1

                    else:
                        print(pos, original_size)
                        rle = struct.unpack('>H', data[pos:pos + 2])[0]
                        pos += 2

                        dist = rle & 0xFFF
                        dstpos = len(out) - (dist + 1)
                        read = (rle >> 12)

                        if (rle >> 12) == 0:
                            read = (data[pos]) + 0x12
                            pos += 1
                        else:
                            read += 2

                        for x in range(read):
                            out.append(out[dstpos + x])
                            out_len += 1

                    code <<= 1
                    bits -= 1

                i = 0
                for byte in out:
                    if type(byte) != bytes:
                        out[i] = byte.to_bytes(1, "big")
                    i += 1

                out = b''.join(out)

                return out


Yaz0.decode("C:\\botw-data\\data\\vol\\content\\Actor\\ActorInfo.product.sbyml")
