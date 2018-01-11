import os


class FileTypes:
    byml = {
        'signature': b'BY\x00\x02',
        'name': 'byml',
    }
    prod = {
        'signature': b'PrOD',
        'name': 'prod'
    }
    aamp = {
        'signature': b'AAMP',
        'name': 'aamp'
    }
    bfev = {
        'signature': b'BFEV',
        'name': 'bfev'
    }
    ffnt = {
        'signature': b'FFNT',
        'name': 'ffnt'
    }
    flan = {
        'signature': b'FLAN',
        'name': 'flan'
    }
    flyt = {
        'signature': b'FLYT',
        'name': 'flyt'
    }
    flim = {
        'signature': b'FLIM',
        'name': 'flim'
    }
    fres = {
        'signature': b'FRES',
        'name': 'fres'
    }
    hknm = {
        'signature': b'W\xe0\xe0W',
        'name': 'hknm',
        'description': 'Havok NavMesh'
    }
    yaz0 = {
        'signature': b'Yaz0',
        'name': 'yaz0'
    }
    fsha = {
        'signature': b'FSHA',
        'name': 'fsha'
    }
    bahs = {
        'signature': b'BAHS',
        'name': 'bahs'
    }
    gfx2 = {
        'signature': b'Gfx2',
        'name': 'gfx2'
    }
    png = {
        'signature': b'\x89PNG',
        'name': 'png'
    }
    hght = {
        'extension': '.hght',
        'name': 'hght'
    }
    extm = {
        'extension': '.extm',
        'name': 'extm'
    }
    mate = {
        'extension': '.mate',
        'name': 'mate'
    }


path = "C:\\botw-data\\decompressed"

list_file_path = os.path.join(path, 'file-types-list.json')


def get_file_type(content, extension):
    if content[0x00:0x04] == FileTypes.byml['signature']:
        return FileTypes.byml['name']

    elif content[0x00:0x04] == FileTypes.prod['signature']:
        return FileTypes.prod['name']

    elif content[0x00:0x04] == FileTypes.aamp['signature']:
        return FileTypes.aamp['name']

    elif content[0x00:0x04] == FileTypes.bfev['signature']:
        return FileTypes.bfev['name']

    elif content[0x00:0x04] == FileTypes.ffnt['signature']:
        return FileTypes.ffnt['name']

    elif content[0x00:0x04] == FileTypes.flan['signature']:
        return FileTypes.flan['name']

    elif content[0x00:0x04] == FileTypes.flyt['signature']:
        return FileTypes.flyt['name']

    elif content[0x00:0x04] == FileTypes.flim['signature']:
        return FileTypes.flim['name']

    elif content[0x00:0x04] == FileTypes.fres['signature']:
        return FileTypes.fres['name']

    elif content[0x00:0x04] == FileTypes.hknm['signature']:
        return FileTypes.hknm['name']

    elif content[0x00:0x04] == FileTypes.yaz0['signature']:
        return FileTypes.yaz0['name']

    elif content[0x00:0x04] == FileTypes.fsha['signature']:
        return FileTypes.fsha['name']

    elif content[0x00:0x04] == FileTypes.bahs['signature']:
        return FileTypes.bahs['name']

    elif content[0x00:0x04] == FileTypes.gfx2['signature']:
        return FileTypes.gfx2['name']

    elif content[0x00:0x04] == FileTypes.png['signature']:
        return FileTypes.png['name']

    elif extension == FileTypes.hght['extension']:
        return FileTypes.hght['name']

    elif extension == FileTypes.extm['extension']:
        return FileTypes.extm['name']

    elif extension == FileTypes.mate['extension']:
        return FileTypes.mate['name']

    else:
        return 'unknown: ' + str(content[0x00:0x04])


with open(list_file_path, 'wb') as list_file:
    list_file.write(b'{"fileStructure" : [')

    for root, subdirs, files in os.walk(path):
        # print('--\n' + root)

        for subdir in subdirs:
            dir_path = os.path.join(root, subdir)

            print('subdirectory ' + subdir)

            list_file.write(('\t{ "path": "%s", "depth": %i, "file": "%s", "type": "%s", "size": %i },\r\n'
                             % (
                                 'vol' + dir_path[25:].replace('\\', '/') + '/',
                                 dir_path[25:].count('\\') - 1,
                                 os.path.basename(os.path.normpath(dir_path[25:].replace('\\', '/'))) + '/',
                                 "dir",
                                 0
                                 )).encode('utf-8'))

        for filename in files:
            file_path = os.path.join(root, filename)

            print('file %s (full path: %s)' % (filename, file_path))

            with open(file_path, 'rb') as f:
                f_content = f.read()
                file_type = get_file_type(f_content, os.path.splitext(file_path)[1])
                file_size = os.path.getsize(file_path)

                list_file.write(('\t{ "path": "%s", "depth": %i, "name": "%s", "type": "%s", "size": %i },\r\n'
                                 % (
                                     file_path[25:].replace('\\', '/'),
                                     file_path[25:].count('\\') - 1,
                                     os.path.basename(file_path),
                                     file_type,
                                     file_size
                                     )).encode('utf-8'))

    list_file.write(b']}')
