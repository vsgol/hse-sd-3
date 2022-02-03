import os
from typing import List, Dict
import subprocess

SUCCESS_RETURN_CODE = 0
FAILED_FILE_OPEN_RETURN_CODE = 1
OTHER_RETURN_CODE = 255


class Command:
    def __init__(self):
        self.return_code = None
        self.stdout = None
        self.stderr = None

    def execute(self, inp: str, memory=None):
        raise NotImplementedError('execute method is not implemented')

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


class DeclareCommand(Command):
    def __init__(self, args):
        super().__init__()
        if len(args) != 2:
            raise ValueError('Declare command must receive exactly 2 arguments')
        self.variable = args[0]
        self.value = args[1]

    def execute(self, inp: str, memory=None):
        if memory is None:
            raise ValueError('Did not get memory reference for DeclareCommand execution')
        memory.set_value(self.variable, self.value)
        self.return_code = SUCCESS_RETURN_CODE
        self.stdout = ''
        self.stderr = ''
        return self.return_code


def get_file_bytes(file_name):
    bs = b''
    stderr = ''
    return_code = SUCCESS_RETURN_CODE
    try:
        if os.path.isdir(file_name):
            raise IsADirectoryError()
        with open(file_name, 'rb') as file:
            bs = file.read()
    except FileNotFoundError:
        stderr = f'cat: {file_name}: No such file or directory'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except IsADirectoryError:
        stderr = f'cat: {file_name}: Is a directory'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except PermissionError:
        stderr = f'cat: {file_name}: Permission denied'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except Exception as e:
        stderr = f'cat: Error while reading file' + str(e)
        return_code = OTHER_RETURN_CODE
    return bs, stderr, return_code


class CatCommand(Command):
    def __init__(self, args):
        super().__init__()
        self.file_name = args[0] if len(args) > 0 else None

    def execute(self, inp: str, memory=None):
        self.stdout = ''
        self.stderr = ''
        if self.file_name is None:
            self.return_code = SUCCESS_RETURN_CODE
            self.stdout = inp
            return self.return_code
        bs, self.stderr, self.return_code = get_file_bytes(self.file_name)
        if self.return_code == SUCCESS_RETURN_CODE:
            self.stdout = bs.decode('utf-8')
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
        super().__init__()
        self.file_name = args[0] if len(args) > 0 else None

    def execute(self, inp: str, memory=None):
        self.stdout = ''
        self.stderr = ''
        if self.file_name is None:
            self.return_code = SUCCESS_RETURN_CODE
            string = inp
            n_bytes = len(string)
        else:
            bs, self.stderr, self.return_code = get_file_bytes(self.file_name)
            if self.return_code != SUCCESS_RETURN_CODE:
                return self.return_code
            n_bytes = len(bs)
            string = bs.decode('utf-8')
        n_words = len(string.split())
        n_lines = len(string.split('\n'))
        self.stdout = '{:6d} {:6d} {:6d}'.format(n_lines, n_words, n_bytes)
        return self.return_code


class PwdCommand(Command):
    def __init__(self, args):
        super().__init__()

    def execute(self, inp: str, memory=None):
        self.stdout = os.path.abspath(os.getcwd())
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code


class ExitCommand(Command):
    def __init__(self, args):
        super().__init__()

    def execute(self, inp: str, memory=None):
        self.stdout = ''
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code

    def is_exit(self):
        return True


class OtherCommand(Command):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def execute(self, inp: str, memory=None):
        if memory is None:
            raise ValueError('Did not get memory reference for OtherCommand execution')
        out = subprocess.Popen(self.args + [inp],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               env=memory.get_env())
        self.stdout, self.stderr = out.communicate()
        if self.stdout is None:
            self.stdout = ''
        else:
            self.stdout = self.stdout.decode('utf-8')
        if self.stderr is None:
            self.stderr = ''
        else:
            self.stderr = self.stderr.decode('utf-8')

        self.return_code = out.returncode
        return self.return_code
