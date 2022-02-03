from typing import List

from .string_processor.parser.command.command import Command


class Executor:
    def __init__(self):
        self.is_terminated = False
        self.last_return_code = None

    def execute(self, pipe: List[Command], memory):
        if len(pipe) == 1 and pipe[0].is_exit():
            self.is_terminated = True
        outputs = []
        errors = []
        for command in pipe:
            self.last_return_code = command.execute(outputs[-1] if len(outputs) > 0 else '', memory)
            outputs.append(command.get_stdout())
            errors.append(command.get_stderr())
        outputs = list(filter(len, outputs))
        errors = list(filter(len, errors))
        return '\n'.join(outputs), '\n'.join(errors)

    def is_shell_terminated(self):
        return self.is_terminated
