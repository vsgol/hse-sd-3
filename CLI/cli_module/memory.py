import os
from typing import Mapping, Iterator


class EnvDict(dict):
    """Dict which returns empty string if there is no key"""
    def __getitem__(self, key):
        res = dict.get(self, key)
        return res if res is not None else ""


class Memory(Mapping[str, str]):
    """Responsible for storing environment variables

        Attributes:
            data: A dict storing environment variables
    """

    def __setitem__(self, key: str, value: str):
        return self.set_value(key, value)

    def __getitem__(self, key: str) -> str:
        return self.get_value(key)

    def __len__(self) -> int:
        return self.data.__len__()

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def __init__(self):
        self.data = EnvDict(os.environ)

    def get_value(self, key):
        """Gets value for key

            Args:
                key: A str for variable name
            Returns:
                A string value for variable if exists. Otherwise returns ''
        """
        return self.data.get(key, '')

    def set_value(self, key, value):
        """Sets value for key

            Args:
                key: A str for variable name
                value: A str for new value of variable
        """
        self.data[key] = value

    def get_env(self):
        """Gets all variables values

            Returns:
                A dict with all variables
        """
        return self.data
