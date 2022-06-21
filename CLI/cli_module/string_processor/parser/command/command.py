import argparse
import io
import os
import re
import subprocess
from abc import ABC, abstractmethod
from contextlib import redirect_stderr

SUCCESS_RETURN_CODE = 0
FAILED_FILE_OPEN_RETURN_CODE = 1
FAILED_ARG_PARSE_RETURN_CODE = 2
OTHER_RETURN_CODE = 255


class Command(ABC):
    """Abstract command class
    Attributes:
        return_code: command return code
        stdout: command output to stdout
        stderr: command output to stderr
    """

    def __init__(self):
        """Inits Command attributes with Nones"""
        self.return_code = None
        self.stdout = None
        self.stderr = None

    @abstractmethod
    def execute(self, inp: str, memory=None):
        """Execution virtual function
        Args:
            inp: Previous command output
            memory: environment variables
        Raises:
            NotImplementedError: method is not overrided or call for abstract command execution
        """
        raise NotImplementedError('execute method is not implemented')

    def get_return_code(self):
        """Returns command return code
        Returns:
            Command exit code if command was executed
        Raises:
            RuntimeError: method was called before command execution
        """
        if self.return_code is None:
            raise RuntimeError('Asking for return code before command execution')
        return self.return_code

    def get_stdout(self):
        """Returns command stdout if command was executed
        Returns:
            Command stdout if command was executed
        Raises:
            RuntimeError: method was called before command execution
        """
        if self.stdout is None:
            raise RuntimeError('Asking for stdout before command execution')
        return self.stdout

    def get_stderr(self):
        """Returns command stderr if command was executed
        Returns:
            Command stderr if command was executed
        Raises:
            RuntimeError: method was called before command execution
        """
        if self.stderr is None:
            raise RuntimeError('Asking for stderr before command execution')
        return self.stderr

    def is_exit(self):
        """Returns whether command was an exit command
        Returns:
            Whether command is an 'exit' command
        """
        return False


class DeclareCommand(Command):
    """Variable value assignment command class
    Attributes:
        variable: target variable name
        value: target variable new value
    """

    def __init__(self, args):
        """Inits DeclareCommand attributes with values from provided arguments
        Args:
            args: Expected to contain two values. First is considered as variable name, second as variable new value
        Raises:
            ValueError: received more or less than two arguments
        """
        super().__init__()
        if len(args) != 2:
            raise ValueError('Declare command must receive exactly 2 arguments')
        self.variable = args[0]
        self.value = args[1]

    def execute(self, inp: str, memory=None):
        """Assigns new value for variable
        Args:
            inp: Previous command output, ignored
            memory: environment variables
        Returns:
            Exit code value
        Raises:
            ValueError: environment was not provided
        """
        if memory is None:
            raise ValueError('Did not get memory reference for DeclareCommand execution')
        memory.set_value(self.variable, self.value)
        self.return_code = SUCCESS_RETURN_CODE
        self.stdout = ''
        self.stderr = ''
        return self.return_code


def get_file_bytes(file_name, calling_command):
    """Reads bytes from file
    Args:
        file_name: target file name
        calling_command: command which called function
    Returns:
        Tuple of read bytes, error message and exit code
    """
    read_bites = b''
    stderr = ''
    return_code = SUCCESS_RETURN_CODE
    try:
        if os.path.isdir(file_name):
            raise IsADirectoryError()
        with open(file_name, 'rb') as file:
            read_bites = file.read()
    except FileNotFoundError:
        stderr = f'{calling_command}: {file_name}: No such file or directory'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except IsADirectoryError:
        stderr = f'{calling_command}: {file_name}: Is a directory'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except PermissionError:
        stderr = f'{calling_command}: {file_name}: Permission denied'
        return_code = FAILED_FILE_OPEN_RETURN_CODE
    except Exception as e:
        stderr = f'{calling_command}: Error while reading file' + str(e)
        return_code = OTHER_RETURN_CODE
    return read_bites, stderr, return_code


class CatCommand(Command):
    """'cat' command class
    Attributes:
        file_name: target file name
    """

    def __init__(self, args):
        """Inits CatCommand file_name if provided
        Args:
            args: Optionally contains target file as first element of the list
        """
        super().__init__()
        self.file_name = args[0] if len(args) > 0 else None

    def execute(self, inp: str, memory=None):
        """Reads file content and outputs it's content
        Args:
            inp: Previous command output, if target file is not provided than outputs this value
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = ''
        self.stderr = ''
        if self.file_name is None:
            self.return_code = SUCCESS_RETURN_CODE
            self.stdout = inp
            return self.return_code
        bs, self.stderr, self.return_code = get_file_bytes(self.file_name, 'cat')
        if self.return_code == SUCCESS_RETURN_CODE:
            self.stdout = bs.decode('utf-8')
        return self.return_code


class EchoCommand(Command):
    """'echo' command class
    Attributes:
        args: strings to output
    """

    def __init__(self, args):
        """Inits EchoCommand args
        Args:
            args: Contains strings for output
        """
        super().__init__()
        self.args = args

    def execute(self, inp: str, memory=None):
        """Outputs command's arguments separated with space
        Args:
            inp: Previous command output, ignored
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = ' '.join(self.args)
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code


class WcCommand(Command):
    """'wc' command class
    Attributes:
        file_name: target file name
    """

    def __init__(self, args):
        """Inits WcCommand file_name if provided
        Args:
            args: Optionally contains target file as first element of the list
        """
        super().__init__()
        self.file_name = args[0] if len(args) > 0 else None

    def execute(self, inp: str, memory=None):
        """Reads file content and outputs it's number of lines, words and bytes
        Args:
            inp: Previous command output, if target file is not provided than outputs statistics for this value
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = ''
        self.stderr = ''
        if self.file_name is None:
            self.return_code = SUCCESS_RETURN_CODE
            n_bytes = len(inp.encode('utf-8'))
            string = inp
        else:
            bs, self.stderr, self.return_code = get_file_bytes(self.file_name, 'wc')
            if self.return_code != SUCCESS_RETURN_CODE:
                return self.return_code
            n_bytes = len(bs)
            string = bs.decode('utf-8')
        if n_bytes == 0:
            n_words, n_lines = 0, 0
        else:
            n_words = len(string.split())
            n_lines = len(string.split('\n'))
        self.stdout = '{:6d} {:6d} {:6d}'.format(n_lines, n_words, n_bytes)
        return self.return_code


class PwdCommand(Command):
    """'pwd' command class"""

    def __init__(self, args):
        """Inits PwdCommand
        Args:
            args: ignored
        """
        super().__init__()

    def execute(self, inp: str, memory=None):
        """Outputs current working directory
        Args:
            inp: Previous command output, ignored
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = os.path.abspath(os.getcwd())
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code


class ExitCommand(Command):
    """'exit' command class"""

    def __init__(self, args):
        """Inits PwdCommand
        Args:
            args: ignored
        """
        super().__init__()

    def execute(self, inp: str, memory=None):
        """No effect
        Args:
            inp: Previous command output, ignored
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = ''
        self.stderr = ''
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code

    def is_exit(self):
        """Signals that the command is 'exit'"""
        return True


class OtherCommand(Command):
    """Any other command class"""

    def __init__(self, args):
        """Inits OtherCommand arguments
        Attributes:
            args: arguments for calling command
        Raises:
            ValueError: trying to create command without command name
        """
        super().__init__()
        if len(args) == 0:
            raise ValueError('At least command name must be provided as argument for OtherCommand')
        self.args = args

    def execute(self, inp: str, memory=None):
        """Executes outer command with provided environment
        Args:
            inp: Previous command output, used as input
            memory: environment variables, used during call
        Returns:
            Exit code value
        Raises:
            ValueError: environment was not provided
        """
        if memory is None:
            raise ValueError('Did not get memory reference for OtherCommand execution')

        try:
            out = subprocess.run(self.args + [inp] if len(inp) > 0 else self.args,
                                 capture_output=True,
                                 env=memory.get_env(), shell=(os.name == 'nt'))
        except Exception as e:
            self.stdout = ''
            self.stderr = str(e)
            self.return_code = OTHER_RETURN_CODE
            return self.return_code

        self.stdout = out.stdout
        self.stderr = out.stderr

        encoding = '866' if os.name == 'nt' else 'utf-8'
        if self.stdout is None:
            self.stdout = ''
        else:
            self.stdout = self.stdout.decode(encoding)
        if self.stderr is None:
            self.stderr = ''
        else:
            self.stderr = self.stderr.decode(encoding)

        self.return_code = out.returncode
        return self.return_code


class GrepCommand(Command):
    """'grep' command class
    Attributes:
        args: arguments to be processed
        parser: argument parser
    """
    def __init__(self, args):
        """Inits GrepCommand arguments and parser
        Args:
            args: contains keys for running grep
        """
        super().__init__()
        self.args = args
        self.parser = argparse.ArgumentParser(prog='grep')
        self.parser.add_argument('-w', dest='word', help='search only for complete word', action='store_true')
        self.parser.add_argument('-i', dest='case_insensitive', help='case-insensitive search', action='store_true')
        self.parser.add_argument('-A', dest='lines_after', help='how many lines print after the match', default=0)

    def execute(self, inp: str, memory=None):
        """Finds target substing in file
        Args:
            inp: Previous command output, if target file is not provided than seeks target in it
            memory: environment variables, ignored
        Returns:
            Exit code value
        """
        self.stdout = ''
        self.stderr = ''

        try:
            f = io.StringIO()
            with redirect_stderr(f):
                args, remaining = self.parser.parse_known_args(self.args)
        except:
            self.stderr = f'Failed to parse grep arguments'
            self.return_code = FAILED_ARG_PARSE_RETURN_CODE
            return self.return_code

        try:
            args.lines_after = int(args.lines_after)
            if args.lines_after < 0:
                raise ValueError
        except ValueError:
            self.stderr = f'Value for -A argument must be non-negative integer'
            self.return_code = FAILED_ARG_PARSE_RETURN_CODE
            return self.return_code

        if len(remaining) == 0:
            self.stderr = f'Not enough arguments for grep'
            self.return_code = FAILED_ARG_PARSE_RETURN_CODE
            return self.return_code

        if len(remaining) == 1:
            text = inp
        else:
            bs, self.stderr, self.return_code = get_file_bytes(remaining[1], 'grep')
            if self.return_code != SUCCESS_RETURN_CODE:
                return self.return_code
            text = bs.decode('utf-8')
        text = text.replace(os.linesep, '\n')
        text = text.split('\n')
        target = remaining[0]
        if args.word:
            target = r'\b{}\b'.format(target)
        result_lines = []
        n_next = 0
        pattern = re.compile(target, re.IGNORECASE if args.case_insensitive else 0)

        for line in text:
            if re.search(pattern, line) is not None:
                result_lines.append(line)
                n_next = args.lines_after
            elif n_next > 0:
                result_lines.append(line)
                n_next -= 1
        self.stdout = '\n'.join(result_lines)
        self.return_code = SUCCESS_RETURN_CODE
        return self.return_code
