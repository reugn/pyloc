import logging
import os.path
from collections import namedtuple

from pyloc.comment_mark import CommentMark
from pyloc.line_handler import LineHandler
from pyloc.line_type import LineType

__all__ = ['FileHandler', 'FileDetails']

FileDetails = namedtuple('FileDetails', 'ext n comment code blank')


class FileHandler(object):

    def __init__(self, name):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._name = str(name)
        self._marks = CommentMark.getByExt(self.__extension)
        self._lh = LineHandler(self._marks)

        self.code = 0
        self.comment = 0
        self.blank = 0

    @property
    def __extension(self) -> str:
        return os.path.splitext(self._name)[1].strip('.')

    def handle(self):
        if self._marks is None:
            return None
        else:
            try:
                h = open(self._name, "r", encoding='ISO-8859-1')
                lines = h.readlines()
                h.close()
                for l in lines:
                    self.__increment(self.__get_line_type(l))
                return FileDetails(self.__extension, 1, self.comment,
                                   self.code, self.blank)
            except IOError:
                self._logger.warning("Failed to parse file %s", self._name)
                return None

    def __get_line_type(self, line) -> LineType:
        trim = line.strip()
        if not trim:
            return LineType.BLANK
        elif (self._lh.handle_multiline(trim) or
              self._lh.handle_single_line(trim)):
            return LineType.COMMENT
        else:
            return LineType.CODE

    def __increment(self, line_type):
        if line_type is LineType.COMMENT:
            self.comment += 1
        elif line_type is LineType.CODE:
            self.code += 1
        else:
            self.blank += 1
