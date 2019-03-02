import logging
import re
from collections import namedtuple

from pyloc.comment_mark import CMT

__all__ = ['LineHandler']

Tags = namedtuple('Tags', 'open close')


class LineHandler(object):
    regex_double_quotes = r'\"(.+?)\"'
    regex_single_quotes = r'\'(.+?)\''

    def __init__(self, marks):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._marks = marks
        self._single_line = self.__fetch_cmt(CMT.SINGLE_LINE)
        self._block_open = self.__fetch_cmt(CMT.BLOCK_OPEN)
        self._block_close = self.__fetch_cmt(CMT.BLOCK_CLOSE)
        self._doc_open = self.__fetch_cmt(CMT.DOC_OPEN)
        self._doc_close = self.__fetch_cmt(CMT.DOC_CLOSE)
        self._at_multiline = None

    def __fetch_cmt(self, cmt_type):
        if self._marks is None:
            return None
        else:
            tags = self._marks.get(cmt_type)
            if tags is None:
                return None
            else:
                return tags if isinstance(tags, list) else [tags]

    @property
    def __is_multi(self):
        return self._block_open is not None and self._block_close is not None

    @property
    def __is_block_opened(self):
        return self.__is_multi and self._at_multiline is CMT.BLOCK_OPEN

    @property
    def __is_doc(self):
        return self._doc_open is not None and self._doc_close is not None

    @property
    def __is_doc_opened(self):
        return self.__is_doc and self._at_multiline is CMT.DOC_OPEN

    def handle_multiline(self, line) -> bool:
        res = False
        if self.__is_multi and not self.__is_doc_opened:
            line = re.sub(LineHandler.regex_double_quotes, "", line)
            line = re.sub(LineHandler.regex_single_quotes, "", line)
            res = self.__handle_by_type(line, Tags(self._block_open,
                                                   self._block_close))
        if not res and self.__is_doc and not self.__is_block_opened:
            res = self.__handle_by_type(line, Tags(self._doc_open,
                                                   self._doc_close))
        return res

    def __handle_by_type(self, line, tags) -> bool:
        if tags.open == tags.close:
            return self.__handle_multiline_same_tags(line, tags)
        else:
            return self.__handle_multiline_diff_tags(line, tags)

    def __handle_multiline_same_tags(self, line, tags) -> bool:
        _tags = sum(line.count(t) for t in tags.open)
        if self._at_multiline is not None:
            if _tags % 2 == 1:
                self._at_multiline = None
            return True
        else:
            if _tags > 0:
                if _tags % 2 == 1 and self.__start_multiline(line, tags.open):
                    self._at_multiline = tags.open
                if line.startswith(tuple(tags.open)):
                    return True
        return False

    def __handle_multiline_diff_tags(self, line, tags) -> bool:
        _open_tag = sum(line.count(t) for t in tags.open)
        _close_tag = sum(line.count(t) for t in tags.close)
        if self._at_multiline is not None:
            if _close_tag > _open_tag:
                self._at_multiline = None
            return True
        else:
            if _open_tag > 0:
                if (_close_tag < _open_tag and
                        self.__start_multiline(line, tags.open)):
                    self._at_multiline = tags.open
                if line.startswith(tuple(tags.open)):
                    return True
        return False

    def __start_multiline(self, line, tag) -> bool:
        if tag is self._block_open:
            return True
        else:
            return line.startswith(tuple(tag))

    def handle_single_line(self, line) -> bool:
        return (self._single_line is not None and
                line.startswith(tuple(self._single_line)))
