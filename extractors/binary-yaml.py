import sys
import yaml

print(yaml.dump({
    'DefaultTimeline': {
        'Nodes': []
    },
    'DisplayDistanceMode': 'None'
}))


class BinaryYaml:
    pass


def main(argv):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
