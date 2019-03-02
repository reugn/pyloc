from argparse import ArgumentParser


class PylocArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(prog='pyloc', usage='%(prog)s [options]')
        super().add_argument("-gi", "--gitignore", action='store_true',
                             help="filter sources by .gitignore file")
        super().add_argument("path", help="working directory")
