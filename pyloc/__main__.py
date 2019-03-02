import sys

from pyloc.processor import Processor


def main():
    print(Processor().process())


if __name__ == '__main__':  # pragma: nocover
    sys.exit(main())
