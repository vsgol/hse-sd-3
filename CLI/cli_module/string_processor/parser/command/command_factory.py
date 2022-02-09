from .command import *


class CommandFactory:
    """Factory for creating Commands instances"""
    def __init__(self):
        """Inits CommandFactory
        Attributes:
            name_to_command: mapping commands names to classes
        """
        self.name_to_command = {
            'cat': CatCommand,
            'echo': EchoCommand,
            'wc': WcCommand,
            'pwd': PwdCommand,
            'exit': ExitCommand
        }

    def tokens_to_commands(self, command_name, args) -> Command:
        """Builds command other from variable assignment
        Args:
            command_name: command name which must be constructed
            args: command arguments
        """
        if command_name not in self.name_to_command:
            return OtherCommand([command_name] + args)
        return self.name_to_command[command_name](args)

    def build_declare_command(self, variable, value) -> Command:
        """Builds variable assignment command
        Args:
            variable: target variable name
            value: target variable new value
        """
        return DeclareCommand([variable, value])

