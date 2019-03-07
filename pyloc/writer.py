import json
from abc import abstractmethod, ABC

from tabulate import tabulate


class Writer(ABC):
    """abstract output writer class"""

    @staticmethod
    @abstractmethod
    def type() -> str:
        """return output format type, auto fills argument choices list"""

    @abstractmethod
    def prepare(self, data, headers) -> str:
        """format data and return output string"""

    def write(self, data, headers):
        print(self.prepare(data, headers))


class TableWriter(Writer):

    @staticmethod
    def type() -> str:
        return "table"

    def prepare(self, data, headers) -> str:
        return tabulate(data, headers=headers, tablefmt="grid")


class JsonWriter(Writer):

    @staticmethod
    def type() -> str:
        return "json"

    def prepare(self, data, headers) -> str:
        zipped = list(map(lambda x: dict(zip(headers, x)), data))
        return json.dumps(zipped)
