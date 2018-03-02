import json
import os

signatures = {
    "b'<?xm'": 'xml',
    "b'\\x00\\x11\"3'": 'eco',
    "b'\\x7fELF'": 'elf',
    "b'\\x89PNG'": 'png',
    "b'AACL'": 'aacl',
    "b'AAMP'": 'aamp',
    "b'AATN'": 'aatn',
    "b'AGST'": 'agst',
    "b'AROC'": 'aroc',
    "b'BAHS'": 'bahs',
    "b'BARS'": 'bars',
    "b'BFEV'": 'bfev',
    "b'BLAL'": 'blal',
    "b'BY\\x00\\x02'": 'byml',
    "b'DDS '": 'dds',
    "b'EFTB'": 'eftb',
    "b'FFNT'": 'ffnt',
    "b'FLAN'": 'flan',
    "b'FLYT'": 'flyt',
    "b'FRES'": 'fres',
    "b'FSAR'": 'fsar',
    "b'FSHA'": 'fsha',
    "b'FSTM'": 'fstm',
    "b'Gfx2'": 'gfx2',
    "b'MsgS'": 'msgs',
    "b'PrOD'": 'prod',
    "b'RSTB'": 'rstb',
    "b'SARC'": 'sarc',
    "b'STAT'": 'stat',
    "b'TSCB'": 'tscb',
    "b'W\\xe0\\xe0W'": 'havok',
    "b'XLNK'": 'xlnk',
    "b'Yaz0'": 'yaz0',
}

file_extensions = {
    '.arc': 'arc',
    '.bflim': 'flim',
    '.btsnd': 'btsnd',
    '.extm': 'extm',
    '.fmc': 'fmc',
    '.h264': 'h264',
    '.hght': 'hght',
    '.jpg': 'jpg',
    '.mate': 'mate',
    '.mp4': 'mp4',
    '.raw': 'raw',
    '.sav': 'sav',
    '.skybin': 'skybin',
    '.tga': 'tga',
    '.txt': 'txt',
    '.xml': 'xml',
}

logger = {
    'file_count': 0,
    'dir_count': 0,
    'average_size': 0,
    'total_size': 0,

    'aacl': 0,
    'aamp': 0,
    'aatn': 0,
    'agst': 0,
    'arc': 0,
    'aroc': 0,
    'bahs': 0,
    'bars': 0,
    'bfev': 0,
    'blal': 0,
    'btsnd': 0,
    'byml': 0,
    'dds': 0,
    'eco': 0,
    'eftb': 0,
    'elf': 0,
    'extm': 0,
    'ffnt': 0,
    'flan': 0,
    'flim': 0,
    'flyt': 0,
    'fmc': 0,
    'fres': 0,
    'fsar': 0,
    'fsha': 0,
    'fstm': 0,
    'gfx2': 0,
    'h264': 0,
    'havok': 0,
    'hght': 0,
    'jpg': 0,
    'mate': 0,
    'mp4': 0,
    'msgs': 0,
    'png': 0,
    'prod': 0,
    'raw': 0,
    'rstb': 0,
    'sarc': 0,
    'sav': 0,
    'skybin': 0,
    'stat': 0,
    'tga': 0,
    'tscb': 0,
    'txt': 0,
    'xlnk': 0,
    'xml': 0,
    'yaz0': 0,

    'unknown': 0,

    'extensions': {}
}


def get_file_types():
    print('Scanning Files...')
    path = "C:\\botw-data\\decompressed\\"

    yaz = open(os.path.dirname(os.path.realpath(__file__)) + '\\yaz0.txt', 'a')
    yaz.close()

    file_structure = read_path(path)

    # Write json data
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\file-types.json', 'w') as json_output:
        print('Saving json...')
        json_output.write(json.dumps(file_structure, sort_keys=True, indent=4, separators=(',', ': ')))

    # Write log file
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\log.txt', 'w') as json_output:
        print('Logging stats...')
        logger['average_size'] = logger['total_size'] / logger['file_count']
        json_output.write(json.dumps(logger, indent=4, separators=(',', ': ')))


def read_path(path):
    file_structure = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for dir_name in dirnames:
            logger['dir_count'] += 1
            file_structure[dir_name] = read_path(dirpath + dir_name + '\\')

        file_structure['files'] = []
        for file_name in filenames:
            file_path = dirpath + file_name

            file_data = {
                'filename': file_name,
                'path': '/vol' + os.path.dirname(os.path.realpath(file_path))[25:].replace('\\', '/') + '/',
                'extension': os.path.splitext(file_name)[1]
            }

            stats = os.stat(file_path)
            file_data['size'] = stats.st_size

            logger['file_count'] += 1
            logger['total_size'] += stats.st_size

            if logger['file_count'] % 1000 == 0:
                print("{0} Files Scanned...".format(logger['file_count']))

            with open(file_path, 'rb') as file:
                file_data['signature'] = str(file.read(0x04))

                if file_data['signature'] in signatures:
                    file_data['type'] = signatures[file_data['signature']]
                    logger[file_data['type']] += 1

                elif file_data['extension'] in file_extensions:
                    file_data['type'] = file_extensions[file_data['extension']]
                    logger[file_data['type']] += 1

                else:
                    file_data['type'] = 'unknown'
                    logger['unknown'] += 1

                # Log file extension types
                if file_data['extension'] in logger['extensions']:
                    logger['extensions'][file_data['extension']]['count'] += 1

                else:
                    logger['extensions'][file_data['extension']] = {
                        'count': 1,
                        'type': file_data['type']
                    }

                if file_data['type'] == 'yaz0':
                    with open(os.path.dirname(os.path.realpath(__file__)) + '\\yaz0.txt', 'a') as yaz:
                        yaz.write(file_path + '\n')

            file_structure['files'].append(file_data)

        break

    return file_structure


def main():
    get_file_types()

    print('Scan Complete!')

    exit(1)


if __name__ == "__main__":
    main()
