from typing import List, Dict

from .formatter import substitute
from .parser import Parser
from .parser.command import Command
from CLI.cli_module.memory import Memory


class StringProcessor:
    """Responsible for splitting the input line into a list of commands"""
    def __init__(self):
        self.parser = Parser()

    def process(self, code: str, memory: Memory) -> List[Command]:
        """Converts the input string into a sequence of commands

        args:
            code (str): input string for processing
            memory (Memory): memory with local variables for substitution

        returns:
            List[Command]: sequence of commands
        """
        code = substitute(code, memory)
        return self.parser.parse(code)
