import datetime

import numpy


def main():
    resource_table = bootstrap_resource_table()
    used_hashes = []

    with open('resource_table.csv', 'w') as resource_table_csv, \
            open('files.csv') as list_file, \
            open('error.log', 'w+') as log_file:
        resource_table_csv.write('"Hash ID","File Name","File Size","Resource Size","Diff","Extension ID","Format ID"\n')

        for row in list_file:
            hash_id, filename, directory, path, size, extension_id, format_id = row.strip().split(',')

            hash_id = int(hash_id.strip('"'))
            path = path.strip('"')
            size = int(size.strip('"'))
            extension_id = int(extension_id.strip('"'))
            format_id = int(format_id.strip('"'))

            if hash_id in resource_table:
                if hash_id not in used_hashes:
                    diff = resource_table[hash_id] - size
                    resource_table_csv.write(
                        '{0},"{1}",{2},{3},{4},{5},{6}\n'.format(hash_id, path, size, resource_table[hash_id], diff, extension_id, format_id))
                    used_hashes.append(hash_id)
            else:
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                log_file.write('{0} - Unable to find hash {1}\n'.format(date, hash_id))

        for hash_id in resource_table:
            if hash_id not in used_hashes:
                resource_table_csv.write('{0},,,{1},,,\n'.format(hash_id, resource_table[hash_id]))


def bootstrap_resource_table():
    rstb = numpy.genfromtxt('resource-table.csv', delimiter=',')
    resource_table = {}
    for row in rstb:
        resource_table[int(row[0])] = int(row[1])
    return resource_table


if __name__ == "__main__":
    main()
