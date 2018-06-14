import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Recursively extracts all SARC files and decompresses all Yaz0 files in Breath of the Wild.')
    parser.add_argument("dirname", type=str, help="Directory to begin extracting")
    args = parser.parse_args()

    unpacker.unpack_all(args.dirname)


if __name__ == "__main__":
    main()