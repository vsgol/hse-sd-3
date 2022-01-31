from typing import List, Dict


class Command:
    def execute(self, args: List[str]):
        pass

    def getReturnCode(self):
        pass

    def getStdout(self):
        pass

    def getStderr(self):
        pass


class DeclCommand(Command):
    def __init__(self, variable: str, value: str, memory: Dict[str, str]):
        pass
