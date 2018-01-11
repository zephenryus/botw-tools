import re

file = open('C:\\botw-data\\src\\extractors\\hash-number.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

hash_table = []

for index in range(0, len(data)):
    match = re.search('(%\d{0,2}d)', data[index])
    if match is not None:
        for sub_index, group in enumerate(match.groups()):
            span = match.span(sub_index)
            sub_match = re.search('(0)([1234])d', group)
            if sub_match is not None:
                length = int(sub_match.groups()[1])
                for count in range(0, 10 ** length):
                    hash_table.append(re.sub('(%\d{0,2}d)', str(count).zfill(length), data[index]))

file = open('C:\\botw-data\\src\\extractors\\hash-number-appendix.txt', 'w')

for value in hash_table:
    file.write("{0}\n".format(value))

file.close()
