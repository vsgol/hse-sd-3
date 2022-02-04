import unittest

from .string_processor.parser.command.command import *
from .executor import Executor


class TestExecutor(unittest.TestCase):
    class Memory:
        def __init__(self):
            self.d = {}

        def set_value(self, name, val):
            self.d[name] = val

        def get_env(self):
            return self.d

    def test_construction(self):
        exe = Executor()
        self.assertIsNone(exe.get_last_return_code())
        self.assertFalse(exe.is_shell_terminated())

    def test_pipe(self):
        exe = Executor()

        mem = self.Memory()

        seqs = [
            [],
            [EchoCommand(['hello'])],
            [EchoCommand(['hello']), EchoCommand(['world']), EchoCommand(['!'])],
            [EchoCommand(['hello']), CatCommand([])],
            [EchoCommand(['hello']), ExitCommand([]), EchoCommand(['!'])],
            [CatCommand(['nosuchfile.txt']), CatCommand(['filekek']), EchoCommand(['!'])],
        ]
        outs = [
            '',
            'hello',
            '!',
            'hello',
            '!',
            '!',
        ]
        errs = [
            '',
            '',
            '',
            '',
            '',
            'cat: nosuchfile.txt: No such file or directory\ncat: filekek: No such file or directory',
        ]

        for seq, tout, terr in zip(seqs, outs, errs):
            out, err = exe.execute(seq, mem)
            self.assertEqual(out, tout)
            self.assertEqual(err, terr)
            self.assertFalse(exe.is_shell_terminated())

    def test_exit(self):
        exe = Executor()
        mem = self.Memory()

        out, err = exe.execute([ExitCommand([])], mem)
        self.assertEqual(out, '')
        self.assertEqual(err, '')
        self.assertTrue(exe.is_shell_terminated())

    def test_assign(self):
        exe = Executor()
        mem = self.Memory()

        name1 = 'name1'
        val1 = 'val1'
        name2 = 'name2'
        val2 = 'val2'
        val3 = 'val3'

        out, err = exe.execute([DeclareCommand([name1, val1])], mem)
        self.assertEqual(out, '')
        self.assertEqual(err, '')
        self.assertFalse(exe.is_shell_terminated())
        self.assertEqual(mem.d[name1], val1)

        out, err = exe.execute([DeclareCommand([name2, val2])], mem)
        self.assertEqual(out, '')
        self.assertEqual(err, '')
        self.assertFalse(exe.is_shell_terminated())
        self.assertEqual(mem.d[name1], val1)
        self.assertEqual(mem.d[name2], val2)

        out, err = exe.execute([DeclareCommand([name1, val3])], mem)
        self.assertEqual(out, '')
        self.assertEqual(err, '')
        self.assertFalse(exe.is_shell_terminated())
        self.assertEqual(mem.d[name1], val3)
        self.assertEqual(mem.d[name2], val2)
