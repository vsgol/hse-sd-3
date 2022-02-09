from cli_module.string_processor.string_processor import StringProcessor
from cli_module.executor import Executor
from cli_module.reader import Reader
from cli_module.writer import Writer
from cli_module.memory import Memory


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
        while True:
            if self.executor.is_shell_terminated():
                break
            input_line = self.reader.get_line()
            commands = self.string_processor.process(input_line, self.memory)
            stdout, stderr = self.executor.execute(commands, self.memory)
            self.writer.print_outputs(stdout, stderr)


if __name__ == '__main__':
    MainApp().start()
