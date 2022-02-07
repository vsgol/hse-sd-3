"""Responsible for splitting the input string into a list of Command"""
from typing import List, Dict

from .formatter import substitute
from .parser import Parser
from .parser.command import Command


class StringProcessor:
    def __init__(self):
        self.parser = Parser()

    def process(self, code: str, memory: Dict[str, str]) -> List[Command]:
        code = substitute(code, memory)
        return self.parser.parse(code)
