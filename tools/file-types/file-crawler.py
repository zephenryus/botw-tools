import atexit
import datetime
import re
import shutil
import tempfile
import traceback

import MySQLdb
import os
import subprocess
import socket

import _mysql_exceptions
import zlib

import src.extractors.sarc


class BotWFileCrawler:
    connection = None
    mysql = None
    dir_name_clear = 29
    start_time = None
    end_time = None

    known_extensions_list = [
        '.agstats',
        '.arc',
        '.baacl',
        '.baatn',
        '.baglblm',
        '.baglccr',
        '.baglclwd',
        '.baglcube',
        '.bagldof',
        '.baglenv',
        '.baglenvset',
        '.baglfila',
        '.bagllmap',
        '.bagllref',
        '.baglmf',
        '.baglshpp',
        '.bagst',
        '.baiprog',
        '.baischedule',
        '.baniminfo',
        '.baroc',
        '.bars',
        '.bas',
        '.baslist',
        '.bassetting',
        '.batcl',
        '.batcllist',
        '.bawareness',
        '.bawntable',
        '.bbonectrl',
        '.bcamanim',
        '.bchemical',
        '.bchmres',
        '.bdemo',
        '.bdgnenv',
        '.bdmgparam',
        '.bdrop',
        '.beco',
        '.belnk',
        '.bfevfl',
        '.bfevtm',
        '.bffnt',
        '.bflan',
        '.bflim',
        '.bflyt',
        '.bfres',
        '.bfsar',
        '.bfsha',
        '.bfstm',
        '.bgapkginfo',
        '.bgapkglist',
        '.bgdata',
        '.bgenv',
        '.bglght',
        '.bgmsconf',
        '.bgparamlist',
        '.bgsdw',
        '.bgsh',
        '.bgsvdata',
        '.bin',
        '.bitemico',
        '.bksky',
        '.blal',
        '.blifecondition',
        '.blod',
        '.blwp',
        '.bmapopen',
        '.bmaptex',
        '.bmodellist',
        '.bmscdef',
        '.bmscinfo',
        '.bnetfp',
        '.bofx',
        '.bphyscharcon',
        '.bphyscontact',
        '.bphysics',
        '.bphyslayer',
        '.bphysmaterial',
        '.bphyssb',
        '.bphyssubmat',
        '.bptclconf',
        '.bquestpack',
        '.brecipe',
        '.breviewtex',
        '.brgbw',
        '.brgcon',
        '.brgconfig',
        '.brgconfiglist',
        '.bsfbt',
        '.bsft',
        '.bshop',
        '.bslnk',
        '.bstftex',
        '.btsnd',
        '.bumii',
        '.bvege',
        '.bwinfo',
        '.bxml',
        '.byaml',
        '.byml',
        '.dds',
        '.elf',
        '.esetlist',
        '.extm',
        '.fmc',
        '.fxparam',
        '.genvres',
        '.gsh',
        '.gtx',
        '.h264',
        '.hght',
        '.hkcl',
        '.hknm2',
        '.hkrb',
        '.hkrg',
        '.hksc',
        '.jpg',
        '.mate',
        '.msbt',
        '.mubin',
        '.png',
        '.raw',
        '.rsizetable',
        '.sav',
        '.sharcb',
        '.skybin',
        '.tga',
        '.tscb',
        '.txt',
        '.xml'
    ]

    extensions_list = []

    signatures_list = {
        "xml": {'format': 'xml', 'index': 0},
        "b'\\x00\\x11\"3'": {'format': 'eco', 'index': 0},
        "b'\\x7fELF'": {'format': 'elf', 'index': 0},
        'extm': {'format': 'extm', 'index': 0},
        "b'\\x89PNG'": {'format': 'png', 'index': 0},
        "b'AACL'": {'format': 'aacl', 'index': 0},
        "b'AAMP'": {'format': 'aamp', 'index': 0},
        "b'AATN'": {'format': 'aatn', 'index': 0},
        "b'AGST'": {'format': 'agst', 'index': 0},
        "aoc": {'format': 'aoc', 'index': 0},
        "b'AROC'": {'format': 'aroc', 'index': 0},
        "b'BAHS'": {'format': 'bahs', 'index': 0},
        "b'BARS'": {'format': 'bars', 'index': 0},
        "b'BFEV'": {'format': 'bfev', 'index': 0},
        "b'BLAL'": {'format': 'blal', 'index': 0},
        "btsnd": {'format': 'btsnd', 'index': 0},
        "b'BY\\x00\\x02'": {'format': 'byml', 'index': 0},
        "b'DDS '": {'format': 'dds', 'index': 0},
        "b'EFTB'": {'format': 'eftb', 'index': 0},
        "b'FFNT'": {'format': 'ffnt', 'index': 0},
        "b'FLAN'": {'format': 'flan', 'index': 0},
        "flim": {'format': 'flim', 'index': 0},
        "b'FLYT'": {'format': 'flyt', 'index': 0},
        'fmc': {'format': 'fmc', 'index': 0},
        "b'FRES'": {'format': 'fres', 'index': 0},
        "b'FSAR'": {'format': 'fsar', 'index': 0},
        "b'FSHA'": {'format': 'fsha', 'index': 0},
        "b'FSTM'": {'format': 'fstm', 'index': 0},
        "b'Gfx2'": {'format': 'gfx2', 'index': 0},
        'h264': {'format': 'h264', 'index': 0},
        'hght': {'format': 'hght', 'index': 0},
        'jpg': {'format': 'jpg', 'index': 0},
        'mate': {'format': 'mate', 'index': 0},
        'mp4': {'format': 'mp4', 'index': 0},
        "b'MsgS'": {'format': 'msgs', 'index': 0},
        "b'PrOD'": {'format': 'prod', 'index': 0},
        'raw': {'format': 'raw', 'index': 0},
        "b'RSTB'": {'format': 'rstb', 'index': 0},
        "b'SARC'": {'format': 'sarc', 'index': 0},
        'sav': {'format': 'sav', 'index': 0},
        'skybin': {'format': 'skybin', 'index': 0},
        "b'STAT'": {'format': 'stat', 'index': 0},
        "b'TSCB'": {'format': 'tscb', 'index': 0},
        'tga': {'format': 'tga', 'index': 0},
        "b'W\\xe0\\xe0W'": {'format': 'havok', 'index': 0},
        "b'XLNK'": {'format': 'xlnk', 'index': 0},
        "b'Yaz0'": {'format': 'yaz0', 'index': 0},
    }

    base_dirs = [
        'Actor',
        'Camera',
        'Demo',
        'Effect',
        'EventFlow',
        'Event',
        'Font',
        'Game',
        'Layout',
        'Local',
        'Map',
        'Model',
        'Movie',
        'NavMesh',
        'Pack',
        'Physics',
        'Sound',
        'Terrain',
        'UI',
        'Voice',
    ]

    def __init__(self, path: str, restart=True, save_to_db=True):
        self.start_time = datetime.datetime.now()
        print("Scan started at {0}".format(self.start_time.strftime("%Y-%m-%d %H:%M:%S.%f")))
        atexit.register(self.on_exit)

        self.mysql_connect()

        if restart and save_to_db:
            self.refresh_database()
            self.init_formats()
            # self.init_hashes()
            self.init_file_system()

        self.scan_dir(path)

    def mysql_connect(self):
        # Check if the server is online
        web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if web_socket.connect_ex(('localhost', 3306)) != 0:
            print('Error: MySQL Server is not currently running...\nMake sure the server is running and retry.')
            exit(0)

        try:
            self.connection = MySQLdb.connect(host='localhost', user='root', password='', database='botwfileexplorer',
                                              charset='utf8')
        except MySQLdb.Error:
            print('Error: Unable to connect to the database even though the MySQL server is currently running...\n'
                  'Try restarting the server and retry.')
            exit(0)

        self.mysql = self.connection.cursor()

    @staticmethod
    def refresh_database() -> None:
        """ Refreshes the Database
        Dumps all previous data and tables and migrates the database schema
        """

        print('Refreshing database...')

        # Run `php artisan migrate:refresh`
        subprocess.run([
            "php",
            "C:\\wamp64\\www\\botw-file-explorer\\artisan",
            "migrate:refresh",
        ])

    def init_formats(self) -> None:
        """ Initialize file formats
        Inserts all known formats (declared as global
        """

        print('Initializing file formats...')

        for index, file_format_name in enumerate(self.signatures_list):
            format_name = self.signatures_list[file_format_name]['format']
            self.signatures_list[file_format_name]['index'] = index + 1

            self.mysql.execute(
                "INSERT INTO `formats` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
                [format_name]
            )
            self.connection.commit()

    def init_hashes(self) -> None:
        print('Initializing hash table...')

        with open('hashed_names.txt', encoding="utf8") as strings_file:
            for line in strings_file:
                line = line.strip()
                string = re.sub(r'[\u0000-\u001f\u0080-\u009f\ufffd]', '', line)
                string = re.sub(r'\s+', ' ', string)

                if not string:
                    continue

                string_hash = zlib.crc32(bytearray(string, 'utf8'))
                hex_hash = hex(string_hash)[2:]
                try:
                    self.mysql.execute(
                        "INSERT INTO `hashes` (`hash`, `hex_hash`, `text`, `created_at`, `updated_at`)"
                        "VALUES (%s, %s, %s, NOW(), NOW())",
                        [
                            string_hash,
                            hex_hash,
                            string
                        ]
                    )
                    self.connection.commit()
                except _mysql_exceptions.IntegrityError:
                    # print((1062, "Duplicate entry '{0}' for key 'hashes_hash_unique'".format(string_hash)))
                    pass

    @staticmethod
    def init_file_system() -> None:
        """ Initializes the files system
        Adds the root directory, /vol/, to the database
        This is needed since it will not scan from the root,
        it starts at /vol/
        """

        print('Initializing file data...')

        # Run `php artisan record:dir vol/ /`
        subprocess.run([
            "php",
            "C:\\wamp64\\www\\botw-file-explorer\\artisan",
            "record:dir",
            'vol/',
            '/'
        ], shell=True, check=True)

    def add_format(self, name: str) -> int:
        """ Add file format to database
        Inserts a new format into the database.
        format name _must_ be unique to the database or will fail

        :param name: The file format name to be added to the database
        :type name: str

        :return: The id (index) of the added format
        :rtype: int

        TODO Add unique constraint exception handler
        """

        # Persist new format to the database
        self.mysql.execute(
            "INSERT INTO `formats` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
            [name]
        )
        self.connection.commit()

        # Add new format to local formats list
        format_index = len(self.signatures_list)
        self.signatures_list[name] = {
            'format': name,
            'index': format_index
        }

        return format_index

    def add_extension(self, name: str) -> int:
        """ Add file extension to database
        Inserts a new extension into the database.
        extension name _must_ be unique to the database or will fail

        :param name: The file extension name to be added to the database
        :type name: str

        :return: The id (index) of the added extension
        :rtype: int

        TODO Add unique constraint exception handler
        """

        # Validate that the name passed is not empty
        if name == '':
            print('ERROR: the extension was invalid or blank!')
            exit(0)

        try:
            # Persist new extension to the database
            self.mysql.execute(
                "INSERT INTO `extensions` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
                [name.replace('s', '', 1)]
            )
            self.connection.commit()
        except _mysql_exceptions.IntegrityError:
            print('{0} already in database'.format(name))

        # Add new format to local extensions list
        self.extensions_list.append(name)

        return len(self.extensions_list)

    @staticmethod
    def get_file_signature(path: str) -> bytes:

        """ Gets the file signature
        Attempts to read the file signature
        Most signatures are stored in the first four bytes of a file

        :param path: Path to the file to read signature
        :type path: str

        :return: First four bytes of file
        :rtype: bytes
        """
        if os.path.exists(path):
            with open(path, 'rb') as file:
                return file.read(0x04)
        else:
            print('\033[31;1mERROR: {0} does not exist.\033[0m'.format(path))

    @staticmethod
    def get_encoded_signature(path: str) -> bytes:
        """ Gets the file signature of a Yaz0 encoded file
        Attempts to read the file signature of the Yaz0 encoded file
        Signatures of encoded files are stored at offset 0x11

        :param path: Path to the file to read signature
        :type path: str

        :return: First four bytes of the encoded file
        :rtype: bytes
        """

        with open(path, 'rb') as file:
            file.seek(0x11)
            return file.read(0x04)

    @staticmethod
    def get_in_memory_file_signature(data):
        return data[0x00:0x04]

    def scan_yaz0(self, path: str):
        if self.get_file_signature(path) == b'Yaz0':
            with open(path, 'rb') as yaz0_file:
                try:
                    decoded = src.extractors.sarc.yaz0_decompress(yaz0_file.read())
                except MemoryError:
                    with open('error.log', 'a+') as log:
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        log.write(
                            "{0} - {1} - MemoryError: {2}\n".format(date, path, traceback.format_exc()))
                        print('\033[0;31mError Logged\033[0m')
                        return ''
                self.scan_in_memory_file(decoded, path)
                return decoded

    def scan_sarc(self, data, path):
        try:
            sarc_archive_output_path = src.extractors.sarc.sarc_extract(data, 1, path)
        except IndexError as e:
            with open('error.log', 'a+') as log:
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                log.write("{0} - {1} - IndexError: {2} - {3}\n".format(date, path, str(e), traceback.format_exc()))
                print('\033[0;31mError Logged\033[0m')
            return

        db_name = sarc_archive_output_path[self.dir_name_clear:].replace('\\', '/').rsplit('/', 1)

        try:
            # Run `php artisan record:dir`
            subprocess.run([
                "php",
                "C:\\wamp64\\www\\botw-file-explorer\\artisan",
                "record:dir",
                db_name[1] + '/',
                db_name[0] + '/'
            ], shell=True, check=True)
        except subprocess.CalledProcessError:
            print('duplicate directory!')

        self.scan_dir(sarc_archive_output_path, True)
        if os.path.exists(sarc_archive_output_path):
            shutil.rmtree(sarc_archive_output_path)

    def scan_in_memory_file(self, decoded: bytearray, path: str):
        filename = os.path.splitext(os.path.basename(path))
        if filename[1][1:2] == 's':
            file_extension = filename[1].split('s', 1)[1]
        else:
            file_extension = filename[1]
        filename = filename[0] + '.' + str(file_extension)

        real_path = os.path.splitext(path[self.dir_name_clear:].replace('\\', '/'))
        if real_path[1][1:2] == 's':
            file_extension = real_path[1].split('s', 1)[1]
        else:
            file_extension = real_path[1]
        real_path = real_path[0] + '.' + str(file_extension)

        extension = os.path.splitext(filename)[1][1:]
        dir_path = path[self.dir_name_clear:].replace('\\', '/').rsplit('/', 1)[0] + '/'
        signature = self.get_in_memory_file_signature(decoded)
        file_format = None

        try:
            file_format = self.signatures_list[str(signature)]
        except KeyError:
            print('Unknown file signature: {0}'.format(signature))

        # Try to see if the extension is already in the extensions list
        try:
            extension_id = self.extensions_list.index(extension) + 1

        # If a ValueError Exception is raised, add the extension to the extensions list and persist
        # the new extension to the database
        except ValueError:
            extension_id = self.add_extension(extension)

        try:
            self.save_file(dir_path, True, extension_id, 'file', filename, file_format['index'], real_path, real_path[13:],len(decoded))
        except TypeError:
            pass
        # self.scan_extra_file_data(decoded, path, file_format['format'])

    def get_format_id(self, extension, signature):
        # Try to match the signature with a format in the signatures_list
        if str(signature) in self.signatures_list:
            format_id = self.signatures_list[str(signature)]['index']

        # If the signatures is not in the list, see if the file extension is
        elif extension in self.signatures_list:
            format_id = self.signatures_list[extension]['index']

        # Otherwise add the format to the database and signatures list
        else:
            format_id = self.add_format(extension)
        return format_id

    def scan_dir(self, path: str, is_archive=False) -> None:
        """ Scan a directory
        Reads all directories and files in the path
        Uses os.walk to recursively walk through all directories and files

        :param is_archive:
        :param path: Path to the directory to begin the scan
        :file_type path: str
        """

        print('Scanning...')

        # Walk the path
        for (dirpath, dirnames, filenames) in os.walk(path):
            # If on Windows strip \ and replace with /
            # Silly Windows
            dir_path = dirpath[self.dir_name_clear:].replace('\\', '/') + '/'

            # Iterate through all directories in the current directory
            for dir_name in dirnames:
                # If on Windows strip \ and replace with /
                name = dir_name.replace('\\', '/') + '/'
                real_path = dir_path + name

                print("Reading {0}...".format(dirpath + name))

                # Persist directory data to the database
                self.mysql.execute(
                    "INSERT INTO `files` (`type`, `name`, `path`, `real_path`, `created_at`, `updated_at`) "
                    "VALUES('dir', %s, %s, %s, NOW(), NOW())",
                    (
                        name,
                        dir_path,
                        real_path,
                    )
                )
                self.connection.commit()

            # Iterate through all files in the current directory
            for filename in filenames:
                real_path = dir_path + filename
                extension = os.path.splitext(filename)[1][1:]
                print("Reading {0}...".format(dirpath + '\\' + filename))

                # Try to see if the extension is already in the extensions list
                try:
                    extension_id = self.extensions_list.index(extension) + 1

                # If a ValueError Exception is raised, add the extension to the extensions list and persist
                # the new extension to the database
                except ValueError:
                    extension_id = self.add_extension(extension)

                signature = self.get_file_signature(dirpath + '\\' + filename)
                encoded = 0
                file_type = 'file'

                # If file is a Yaz0 encoded, mark and encoded and set file_type to archive
                if signature == b'Yaz0':
                    encoded = 1
                    file_type = 'arc'
                    decoded = self.scan_yaz0(dirpath + '\\' + filename)

                    # If the file is a Yaz0 encoded SARC, just label it as a SARC
                    # because sarc's are almost always Yaz0 encoded
                    if self.get_encoded_signature(dirpath + '\\' + filename) == b'SARC':
                        signature = b'SARC'
                        self.scan_sarc(decoded, dirpath + '\\' + filename)

                format_id = self.get_format_id(extension, signature)
                filesize = os.path.getsize(dirpath + '\\' + filename)
                hash_name = self.get_hash_name(real_path, is_archive)

                self.save_file(dir_path, encoded, extension_id, file_type, filename, format_id, real_path,
                               hash_name, filesize)

    def save_file(self, dir_path, encoded, extension_id, file_type, filename, format_id, real_path, hash_name,
                  filesize):
        try:
            # Persist file data to the database
            self.mysql.execute(
                "INSERT INTO `files` (`type`, `extension_id`, `format_id`, `encoded`, `name`, `path`, `real_path`,"
                "`hash`, `hex_hash`, `size`, `created_at`, `updated_at`) VALUES(%s, %s, %s, %s, %s, %s, %s, CRC32(%s),"
                "HEX(CRC32(%s)), %s, NOW(), NOW())",
                (
                    file_type,
                    extension_id,
                    format_id,
                    encoded,
                    filename,
                    # dir_path,
                    hash_name,
                    real_path,
                    hash_name,
                    hash_name,
                    filesize
                )
            )
            self.connection.commit()
        except _mysql_exceptions.IntegrityError:
            print('duplicate!')

    def scan_extra_file_data(self, decoded, path, file_format):
        if file_format == 'prod':
            self.scan_prod(decoded, path)
        elif file_format == 'byml':
            self.scan_byml(decoded, path)

    @staticmethod
    def scan_prod(decoded, path):
        import src.tools.terrain.prod

        with tempfile.NamedTemporaryFile('wb') as temp_file:
            print('Scanning PrOD data...')
            temp_file.write(decoded)
            prod = src.tools.terrain.prod.PrOD(temp_file.name, decoded)

        for obj in prod.data_object:
            print(obj)

    def scan_byml(self, decoded, path):
        import src.extractors.byaml

        with tempfile.NamedTemporaryFile('wb') as temp_file:
            print('Scanning BYML data...')
            temp_file.write(decoded)
            byml = src.extractors.byaml.BYML(temp_file.name, decoded)

        byml_objects = self.scan_byml_objects(byml.data_object)

        print(byml.data_object, byml_objects)
        exit()

        pass

    def scan_byml_objects(self, byml_data_object):
        data_object = []
        # TODO Read data object recursively to get hashID, SRTHash and UnitConfigName
        for byml_object in byml_data_object:
            if isinstance(byml_object, dict) or isinstance(byml_object, list):
                data_object.append(self.scan_byml_objects(byml_data_object[byml_object]))
            else:
                data_object.append(byml_object)

        return data_object

    def on_exit(self):
        self.end_time = datetime.datetime.now()
        delta = self.end_time - self.start_time
        print("Scan took {0} seconds".format(delta.total_seconds()))

    def get_hash_name(self, path, is_archive):
        if is_archive:
            path = path.split('.', 1)[1].split('/', 1)[1]
            print(path)

        for base_dir in self.base_dirs:
            if base_dir in path:
                return '{0}{1}'.format(base_dir, path.split(base_dir, 1)[1])
            else:
                with open('error.log', 'a+') as log:
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    log.write("{0} - Base dir not in list: {0}\n".format(date, path))
        return ''


def main() -> None:
    # BotWFileCrawler("C:\\botw-data\\data\\vol")
    # BotWFileCrawler("C:\\botw-data\\data\\vol\\content\\Model")
    BotWFileCrawler("C:\\botw-data\\data\\1.5.0 - 3.0\\vol")
    exit(1)


if __name__ == "__main__":
    main()
