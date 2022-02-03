class StringProcessor:
    def process(self, input):
        return ['echo 1', 'exit']


class Executor:
    def execute(self, commands, memory):
        return 'output', 'errors'

    def is_shell_terminated(self):
        return True