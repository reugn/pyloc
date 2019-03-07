from enum import Enum

__all__ = ['CMT', 'CommentMark']


class CMT(Enum):
    """Comment symbols Enum"""

    # Single line comment symbol
    SINGLE_LINE = 1

    # Block comment opening symbol
    BLOCK_OPEN = 2

    # Block comment closing symbol
    BLOCK_CLOSE = 3

    # Doc comment opening symbol
    # Requires first character of a line positioning
    DOC_OPEN = 4

    # Doc comment closing symbol
    # Requires first character of a line positioning
    DOC_CLOSE = 5


class CommentMark:

    @classmethod
    def getByExt(cls, ext) -> dict:
        """return comment symbols by file extension"""
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

    __css_list = {
        CMT.BLOCK_OPEN: "/*",
        CMT.BLOCK_CLOSE: "*/",
    }

    __html_list = {
        CMT.BLOCK_OPEN: "<!--",
        CMT.BLOCK_CLOSE: "-->",
    }

    # Supported file extensions list
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
        "dart": __c_style_list,
        "hs": {
            CMT.SINGLE_LINE: ["--"],
            CMT.DOC_OPEN: "{-",
            CMT.DOC_CLOSE: "-}",
        },
        "lua": {
            CMT.SINGLE_LINE: ["--"],
            CMT.DOC_OPEN: "--[[",
            CMT.DOC_CLOSE: "]]",
        },
        "erl": {CMT.SINGLE_LINE: ["%"]},
        "hrl": {CMT.SINGLE_LINE: ["%"]},

        "c": __c_style_list,
        "cpp": __c_style_list,
        "h": __c_style_list,
        "cs": __c_style_list,
        "vb": {
            CMT.SINGLE_LINE: ["'", "'''"],
        },
        "fs": {
            CMT.SINGLE_LINE: ["//"],
            CMT.BLOCK_OPEN: "(*",
            CMT.BLOCK_CLOSE: "*)",
        },

        "go": __c_style_list,
        "rs": __c_style_list,

        "swift": __c_style_list,
        "m": __c_style_list,

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
        "ts": __c_style_list,
        "html": __html_list,
        "htm": __html_list,
        "css": __css_list,
        "less": __css_list,
        "scss": __css_list,
        "sass": __css_list,

        "sh": __shell_list,
    }
