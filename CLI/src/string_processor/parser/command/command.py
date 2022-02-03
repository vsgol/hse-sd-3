import os
from typing import List, Dict

SUCCESS_RETURN_CODE = 0
FAILED_FILE_OPEN_RETURN_CODE = 1
OTHER_RETURN_CODE = 255


class Command:
    def __init__(self):
        self.return_code = None
        self.stdout = None
        self.stderr = None

    def execute(self, inp: str, memory=None):
        raise NotImplementedError('Execute method is not implemented')

    def get_return_code(self):
        if self.return_code is None:
            raise RuntimeError('Asking for return code before command execution')
        return self.return_code

    def get_stdout(self):
        if self.stdout is None:
            raise RuntimeError('Asking for stdout before command execution')
        return self.stdout

    def get_stderr(self):
        if self.stderr is None:
            raise RuntimeError('Asking for stderr before command execution')
        return self.stderr

    def is_exit(self):
        return False


class DeclCommand(Command):
    def __init__(self, variable: str, value: str, memory):
        super().__init__()
        self.variable = variable
        self.value = value

    def execute(self, inp: str, memory=None):
        if memory is None:
            raise ValueError('Did not get memory reference for DeclCommand execution')
        memory.set_value(self.variable, self.value)
        self.return_code = SUCCESS_RETURN_CODE
        self.stdout = ''
        self.stderr = ''
        return self.return_code


class CatCommand(Command):
    def __init__(self, args):
        super().__init__()
        self.file_name = args[0] if len(args) > 0 else None

    def execute(self, inp: str, memory=None):
        self.stdout = ''
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        if self.file_name is None:
            self.return_code = SUCCESS_RETURN_CODE
            self.stdout = inp
            return
        try:
            if os.path.isdir(self.file_name):
                raise IsADirectoryError()
            with open(self.file_name, 'rb') as file:
                self.stdout = file.read().decode("utf-8")
        except FileNotFoundError:
            self.stderr = f'cat: {self.file_name}: No such file or directory'
            self.return_code = FAILED_FILE_OPEN_RETURN_CODE
        except IsADirectoryError:
            self.stderr = f'cat: {self.file_name}: Is a directory'
            self.return_code = FAILED_FILE_OPEN_RETURN_CODE
        except PermissionError:
            self.stderr = f'cat: {self.file_name}: Permission denied'
            self.return_code = FAILED_FILE_OPEN_RETURN_CODE
        except Exception as e:
            self.stderr = f'cat: Error while reading file' + str(e)
            self.return_code = OTHER_RETURN_CODE
        return self.return_code


class EchoCommand(Command):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def execute(self, inp: str, memory=None):
        self.stdout = ' '.join(self.args)
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code


class WcCommand(Command):
    def __init__(self, args):
        pass

    def execute(self, inp: str, memory=None):
        pass


class PwdCommand(Command):
    def __init__(self, args):
        pass

    def execute(self, inp: str, memory=None):
        pass


class OtherCommand(Command):
    def __init__(self, args):
        pass

    def execute(self, inp: str, memory=None):
        pass

    def is_exit(self):
        return True
