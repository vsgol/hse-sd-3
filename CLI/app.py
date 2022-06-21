from cli_module import Reader, Writer, Memory, StringProcessor, Executor


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
                    print()
                    continue
                try:
                    commands = self.string_processor.process(input_line, self.memory)
                except ValueError as e:
                    self.writer.print_outputs('', f'Failed to substitute variables: {e!s}')
                    continue
                except Exception as e:
                    self.writer.print_outputs('', f'Failed to parse input: {e!s}')
                    continue
                try:
                    stdout, stderr = self.executor.execute(commands, self.memory)
                except Exception as e:
                    self.writer.print_outputs('', 'Failed to execute commands ' + str(e))
                    continue
                self.writer.print_outputs(stdout, stderr)
        except Exception as e:
            self.writer.print_outputs('', 'Terminating CLI. ' + str(e))


if __name__ == '__main__':
    MainApp().start()
