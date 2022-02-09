import unittest

from .command import *
from .command_factory import CommandFactory


class TestFactory(unittest.TestCase):
    def test_predefined(self):
        factory = CommandFactory()

        self.assertTrue(isinstance(factory.tokens_to_commands('cat', ['hello.txt']), CatCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('cat', []), CatCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('wc', ['hello.txt']), WcCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('wc', []), WcCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('echo', ['hello.txt', 'hello']), EchoCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('pwd', ['hello.txt']), PwdCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('exit', ['exit']), ExitCommand))

    def test_other(self):
        factory = CommandFactory()

        self.assertTrue(isinstance(factory.tokens_to_commands('git', ['clone', 'some_url']), OtherCommand))
        self.assertTrue(isinstance(factory.tokens_to_commands('gcc', ['compile_me.cpp']), OtherCommand))

    def test_assign(self):
        name = 'name'
        val = 'val'

        factory = CommandFactory()

        self.assertTrue(isinstance(factory.tokens_to_commands(name, [val]), OtherCommand))
        self.assertTrue(isinstance(factory.build_declare_command(name, val), DeclareCommand))
