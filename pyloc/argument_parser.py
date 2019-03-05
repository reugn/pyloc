import logging
from argparse import ArgumentParser

from pyloc.writer import Writer


class PylocArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(prog='pyloc', usage='%(prog)s [options]')
        super().add_argument("path", help="working directory")
        super().add_argument("-gi", "--gitignore", action='store_true',
                             help="filter sources by .gitignore file")
        super().add_argument("-s", "--sort", default='files',
                             choices=['files', 'comment', 'code', 'blank'],
                             help="sort results by field")
        super().add_argument("-o", "--out", default='table',
                             choices=self._get_formats(),
                             help="output format")

    @staticmethod
    def _get_formats() -> list:
        return [cls.type() for cls in Writer.__subclasses__()]


class Args(object):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._arg_parser = PylocArgumentParser()
        self.headers = ['File Ext', 'Files', 'Comment', 'Code', 'Blank']
        self.ignore_dirs = []
        self.ignore_files = []
        self.parse_flags()

    @staticmethod
    def __ignore_files(lines) -> list:
        def file_pattern(l):
            return not (l.lstrip().startswith("#") or l.endswith('/') or not l)

        lines = list(filter(lambda l: file_pattern(l), lines))
        return lines

    @staticmethod
    def __ignore_dirs(lines) -> list:
        lines = [l for l in lines if l.endswith('/')]
        lines = [l[:-1] for l in lines]
        extended = ["./" + f for f in lines if not f.startswith("./")]
        return lines + extended + ["./.git"]

    def _sort(self, _list) -> list:
        return sorted(_list, key=lambda x: x[self._sort_by], reverse=True)

    def prepare(self, data) -> str:
        _sorted = self._sort(data)
        return self._writer.prepare(_sorted, self.headers)

    def parse_flags(self):
        flags = self._arg_parser.parse_args()
        if flags.gitignore:
            try:
                lines = [line.rstrip('\n') for line in open('.gitignore')]
                self.ignore_dirs = self.__ignore_dirs(lines)
                self.ignore_files = self.__ignore_files(lines)
            except OSError:
                self._logger.warning("No .gitignore file found")
        self.dir = flags.path
        self._sort_by = list(map(lambda x: x.lower(), self.headers)).index(flags.sort)
        self._writer = filter(lambda cls: cls.type() == flags.out,
                              Writer.__subclasses__()).__next__()()
