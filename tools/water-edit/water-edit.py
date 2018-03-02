file = "C:\\botw-data\\src\\tools\\water-edit\\5000000000.water.extm.hex"

with open(file, 'rb') as file:
    with open("C:\\botw-data\\src\\tools\\water-edit\\5000000000.water.extm\\5000000000.water.extm", 'rb+') as output:
        for index in range(0, 4096):
            output.write(file.read(0x01))
            output.write(b'\xff')
            file.seek(0x01, 1)
            output.write(file.read(0x06))

exit(1)
