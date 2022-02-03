from .command import *


class CommandFactory:
    def __init__(self):
        self.name_to_command = {
            'cat': CatCommand,
            'echo': EchoCommand,
            'wc': WcCommand,
            'pwd': PwdCommand,
            'exit': ExitCommand
        }

    def tokens_to_commands(self, command_name, args) -> Command:
        if command_name not in self.name_to_command:
            return OtherCommand([command_name] + args)
        return self.name_to_command[command_name](args)

    def build_declare_command(self, variable, value) -> Command:
        return DeclareCommand([variable, value])

