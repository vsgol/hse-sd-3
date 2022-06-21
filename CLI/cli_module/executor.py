from typing import List

from .string_processor.parser.command.command import Command


class Executor:
    """Class for pipeline execution"""
    def __init__(self):
        """Inits Executor
        Attributes:
            is_terminated: flag whether application must be terminated
            last_return_code: last executed command return code
        """
        self.is_terminated = False

    def execute(self, pipe: List[Command], memory):
        """Executes the sequence of commands
        Args:
            pipe: target sequence of commands to be executed
            memory: environments variables
        Returns:
            Separated with break lines non-empty commands' outputs and error messages
        """
        if len(pipe) == 1 and pipe[0].is_exit():
            self.is_terminated = True
        outputs = []
        errors = []
        for command in pipe:
            self.last_return_code = command.execute(outputs[-1] if len(outputs) > 0 else '', memory)
            outputs.append(command.get_stdout())
            errors.append(command.get_stderr())
        # Remove empty strings
        errors = list(filter(len, errors))
        return outputs[-1] if len(outputs) > 0 else '', '\n'.join(errors)

    def is_shell_terminated(self):
        """Indicated whether application must be terminated"""
        return self.is_terminated
