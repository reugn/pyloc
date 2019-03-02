from enum import Enum

__all__ = ['LineType']


class LineType(Enum):
    CODE = 1
    COMMENT = 2
    BLANK = 3
