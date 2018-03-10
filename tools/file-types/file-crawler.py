import MySQLdb
import os
import subprocess

# Global variables
connection = MySQLdb.connect(host='localhost', user='root', password='', database='botwfileexplorer')
mysql = connection.cursor()

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


def init_formats() -> None:
    """ Initialize file formats
    Inserts all known formats (declared as global
    """

    global mysql, connection, signatures_list

    print('Initializing file formats...')

    for index, file_format_name in enumerate(signatures_list):
        format_name = signatures_list[file_format_name]['format']
        signatures_list[file_format_name]['index'] = index + 1

        mysql.execute(
            "INSERT INTO `formats` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
            [format_name]
        )
        connection.commit()


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


def add_format(name: str) -> int:
    """ Add file format to database
    Inserts a new format into the database.
    format name _must_ be unique to the database or will fail

    :param name: The file format name to be added to the database
    :type name: str

    :return: The id (index) of the added format
    :rtype: int

    TODO Add unique constraint exception handler
    """

    global mysql, connection, signatures_list

    # Persist new format to the database
    mysql.execute(
        "INSERT INTO `formats` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
        [name]
    )
    connection.commit()

    # Add new format to local formats list
    format_index = len(signatures_list)
    signatures_list[name] = {
        'format': name,
        'index': format_index
    }

    return format_index


def add_extension(name: str) -> int:
    """ Add file extension to database
    Inserts a new extension into the database.
    extension name _must_ be unique to the database or will fail

    :param name: The file extension name to be added to the database
    :type name: str

    :return: The id (index) of the added extension
    :rtype: int

    TODO Add unique constraint exception handler
    """

    global mysql, connection, signatures_list

    # Validate that the name passed is not empty
    if name == '':
        print('ERROR: the extension was invalid or blank!')
        exit(0)

    # Persist new extension to the database
    mysql.execute(
        "INSERT INTO `extensions` (`name`, `created_at`, `updated_at`) VALUES (%s, NOW(), NOW())",
        [name]
    )
    connection.commit()

    # Add new format to local extensions list
    extensions_list.append(name)

    return len(extensions_list)


def get_file_signature(path: str) -> bytes:
    """ Gets the file signature
    Attempts to read the file signature
    Most signatures are stored in the first four bytes of a file

    :param path: Path to the file to read signature
    :type path: str

    :return: First four bytes of file
    :rtype: bytes
    """
    with open(path, 'rb') as file:
        return file.read(0x04)


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


def scan_dir(path: str) -> None:
    """ Scan a directory
    Reads all directories and files in the path
    Uses os.walk to recursively walk through all directories and files

    :param path: Path to the directory to begin the scan
    :file_type path: str
    """

    global mysql, connection, signatures_list

    print('Scanning...')

    # Walk the path
    for (dirpath, dirnames, filenames) in os.walk(path):
        # If on Windows strip \ and replace with /
        # Silly Windows
        dir_path = dirpath[17:].replace('\\', '/') + '/'

        # Iterate through all directories in the current directory
        for dir_name in dirnames:
            # If on Windows strip \ and replace with /
            name = dir_name.replace('\\', '/') + '/'
            real_path = dir_path + name

            print("Reading {0}...".format(real_path))

            # Persist directory data to the database
            mysql.execute(
                "INSERT INTO `files` (`file_type`, `name`, `path`, `real_path`, `created_at`, `updated_at`) VALUES('dir', %s, %s, %s, NOW(), NOW())",
                (
                    name,
                    dir_path,
                    real_path,
                )
            )
            connection.commit()

        # Iterate through all files in the current directory
        for filename in filenames:
            real_path = dir_path + filename
            extension = os.path.splitext(filename)[1][1:]
            print("Reading {0}...".format(real_path))

            # Try to see if the extension is already in the extensions list
            try:
                extension_id = extensions_list.index(extension) + 1

            # If a ValueError Exception is raised, add the extension to the extensions list and persist
            # the new extension to the database
            except ValueError:
                extension_id = add_extension(extension)

            signature = get_file_signature(dirpath + '\\' + filename)
            encoded = 0
            file_type = 'file'

            # If file is a Yaz0 encoded, mark and encoded and set file_type to archive
            if signature == b'Yaz0':
                encoded = 1
                file_type = 'arc'

                # If the file is a Yaz0 encoded SARC, just label it as a SARC
                # because sarc's are almost always Yaz0 encoded
                if get_encoded_signature(dirpath + '\\' + filename) == b'SARC':
                    signature = b'SARC'

            # Try to match the signature with a format in the signatures_list
            if str(signature) in signatures_list:
                format_id = signatures_list[str(signature)]['index']

            # If the signatures is not in the list, see if the file extension is
            elif extension in signatures_list:
                format_id = signatures_list[extension]['index']

            # Otherwise add the format to the database and signatures list
            else:
                format_id = add_format(extension)

            # Persist file data to the database
            mysql.execute(
                "INSERT INTO `files` (`file_type`, `extension_id`, `format_id`, `encoded`, `name`, `path`, `real_path`, `created_at`, `updated_at`) VALUES(%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())",
                (
                    file_type,
                    extension_id,
                    format_id,
                    encoded,
                    filename,
                    dir_path,
                    real_path
                )
            )
            connection.commit()


def main() -> None:
    refresh_database()
    init_formats()
    init_file_system()
    scan_dir("C:\\botw-data\\data\\vol")

    exit(1)


if __name__ == "__main__":
    main()
