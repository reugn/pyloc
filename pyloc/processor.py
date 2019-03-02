import concurrent.futures
import logging
import os
from collections import defaultdict
from fnmatch import fnmatch

from tabulate import tabulate

from pyloc.argument_parser import PylocArgumentParser
from pyloc.file_handler import FileDetails, FileHandler


class Processor(object):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._arg_parser = PylocArgumentParser()
        self._ignore_dirs = []
        self._ignore_files = []
        self.__parse_flags()

    def process(self):
        lines = []
        for root, dirs, files in os.walk(self._dir):
            if root in self._ignore_dirs:
                dirs[:] = []
            else:
                files = self.__filter_files_by_ignore_list(files)
                files = [os.path.join(os.path.abspath(root), f) for f in files]
                rt = self.__read_parallel(files)
                lines.extend(filter(None.__ne__, rt))

        merged = defaultdict(lambda: [0, 0, 0, 0])
        for ext, *values in lines:
            merged[ext] = [sum(i) for i in zip(values, merged[ext])]

        grouped = []
        for k, v in merged.items():
            grouped.append([k] + v)

        _sorted = sorted(grouped, key=lambda x: x[1], reverse=True)

        headers = ['File Ext', 'Files', 'Comment', 'Code', 'Blank']
        return tabulate(_sorted, headers=headers, tablefmt="grid")

    def __read_parallel(self, file_names):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.__handle_file, f)
                       for f in file_names]
            return [fut.result() for fut in futures]

    @staticmethod
    def __handle_file(file_path) -> FileDetails:
        return FileHandler(file_path).handle()

    def __filter_files_by_ignore_list(self, filenames) -> list:
        for ignore in self._ignore_files:
            filenames = [n for n in filenames if not fnmatch(n, ignore)]
        return filenames

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

    def __parse_flags(self):
        flags = self._arg_parser.parse_args()
        if flags.gitignore:
            try:
                lines = [line.rstrip('\n') for line in open('.gitignore')]
                self._ignore_dirs = self.__ignore_dirs(lines)
                self._ignore_files = self.__ignore_files(lines)
            except OSError:
                self._logger.warning("No .gitignore file found")
        self._dir = flags.path
