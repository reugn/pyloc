import concurrent.futures
import logging
import os
from collections import defaultdict
from fnmatch import fnmatch

from tabulate import tabulate

from pyloc.argument_parser import Args
from pyloc.file_handler import FileDetails, FileHandler


class Processor(object):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._args = Args()

    def process(self):
        lines = []
        for root, dirs, files in os.walk(self._args.dir):
            if root in self._args.ignore_dirs:
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

        _sorted = self._args.sort(grouped)

        return tabulate(_sorted, headers=self._args.headers, tablefmt="grid")

    def __read_parallel(self, file_names):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.__handle_file, f)
                       for f in file_names]
            return [fut.result() for fut in futures]

    @staticmethod
    def __handle_file(file_path) -> FileDetails:
        return FileHandler(file_path).handle()

    def __filter_files_by_ignore_list(self, filenames) -> list:
        for ignore in self._args.ignore_files:
            filenames = [n for n in filenames if not fnmatch(n, ignore)]
        return filenames
