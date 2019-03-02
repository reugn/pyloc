from enum import Enum

__all__ = ['CMT', 'CommentMark']


class CMT(Enum):
    """
    Single line comment symbol
    """
    SINGLE_LINE = 1

    """
    Block comment opening symbol
    """
    BLOCK_OPEN = 2

    """
    Block comment closing symbol
    """
    BLOCK_CLOSE = 3

    """
    Doc comment opening symbol
    Requires first character of a line positioning
    """
    DOC_OPEN = 4

    """
    Doc comment closing symbol
    Requires first character of a line positioning
    """
    DOC_CLOSE = 5


class CommentMark:

    @classmethod
    def getByExt(cls, ext) -> dict:
        return cls.__mark_list.get(ext)

    __empty_list = {}

    __shell_list = {
        CMT.SINGLE_LINE: ["#"],
    }

    __c_style_list = {
        CMT.SINGLE_LINE: ["//"],
        CMT.BLOCK_OPEN: "/*",
        CMT.BLOCK_CLOSE: "*/",
    }

    """
    Supported file extensions list
    """
    __mark_list = {
        "py": {
            CMT.SINGLE_LINE: ["#"],
            CMT.DOC_OPEN: ["'''", '"""'],
            CMT.DOC_CLOSE: ["'''", '"""'],
        },

        "scala": __c_style_list,
        "java": __c_style_list,
        "kt": __c_style_list,
        "clj": {
            CMT.SINGLE_LINE: [";;"],
        },
        "groovy": __c_style_list,

        "hs": {
            CMT.SINGLE_LINE: ["--"],
            CMT.DOC_OPEN: "{-",
            CMT.DOC_CLOSE: "-}",
        },

        "c": __c_style_list,
        "cpp": __c_style_list,
        "h": __c_style_list,
        "cs": __c_style_list,

        "go": __c_style_list,
        "rs": __c_style_list,

        "php": __c_style_list,
        "rb": {
            CMT.SINGLE_LINE: ["#"],
            CMT.DOC_OPEN: "=begin",
            CMT.DOC_CLOSE: "=end",
        },
        "pl": {
            CMT.SINGLE_LINE: ["#"],
            CMT.DOC_OPEN: "=begin",
            CMT.DOC_CLOSE: "=end",
        },

        "js": __c_style_list,
        "html": {
            CMT.BLOCK_OPEN: "<!--",
            CMT.BLOCK_CLOSE: "-->",
        },
        "css": {
            CMT.BLOCK_OPEN: "/*",
            CMT.BLOCK_CLOSE: "*/",
        },

        "sh": __shell_list,
    }
