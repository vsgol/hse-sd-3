from CLI.src.plug import StringProcessor
from CLI.src.plug import Executor
from CLI.src.reader import Reader
from CLI.src.writer import Writer
from CLI.src.memory import Memory


class MainApp:
    """Responsible for linking the application components and interacting with the user

        Attributes:
            reader:
            writer:
            memory:
            string_processor:
            executor:
    """

    def __init__(self):
        self.reader = Reader()
        self.writer = Writer()
        self.memory = Memory()
        self.string_processor = StringProcessor()
        self.executor = Executor()

    def start(self):
        """Runs process"""
        while True:
            if self.executor.is_shell_terminated():
                break
            input_line = self.reader.get_line()
            commands = self.string_processor.process(input_line)
            stdout, stderr = self.executor(commands)
            self.writer.print_outputs(stdout, stderr)
