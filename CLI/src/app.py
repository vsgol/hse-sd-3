from CLI.src.string_processor.string_processor import StringProcessor
from CLI.src.executor import Executor
from CLI.src.reader import Reader
from CLI.src.writer import Writer
from CLI.src.memory import Memory


class MainApp:
    """Responsible for linking the application components and interacting with the user

        Attributes:
            reader: reads user input
            writer: writes result of execution
            memory: stores environmental variables
            string_processor: converts input to commands
            executor: executes commands
    """

    def __init__(self):
        self.reader = Reader()
        self.writer = Writer()
        self.memory = Memory()
        self.string_processor = StringProcessor()
        self.executor = Executor()

    def start(self):
        """Runs process"""
        try:
            while True:
                if self.executor.is_shell_terminated():
                    break
                try:
                    input_line = self.reader.get_line()
                except KeyboardInterrupt:
                    continue
                try:
                    commands = self.string_processor.process(input_line)
                except Exception:
                    self.writer.print_outputs('', 'Failed to parse input')
                    continue
                try:
                    stdout, stderr = self.executor.execute(commands, memory)
                except Exception:
                    self.writer.print_outputs('', 'Failed to execute commands')
                    continue
                self.writer.print_outputs(stdout, stderr)
        except Exception:
            self.writer.print_outputs('', 'Failed to read input')


if __name__ == '__main__':
    MainApp().start()
