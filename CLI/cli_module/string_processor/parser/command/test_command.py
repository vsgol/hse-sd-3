import unittest

from .command import *


class TestCommands(unittest.TestCase):
    def check_commands_common(self, cmd):
        with self.assertRaises(RuntimeError):
            cmd.get_stdout()
        with self.assertRaises(RuntimeError):
            cmd.get_return_code()
        with self.assertRaises(RuntimeError):
            cmd.get_stderr()

        self.assertEqual(cmd.is_exit(), isinstance(cmd, ExitCommand))

    def test_abstract_command(self):
        cmd = Command()

        self.assertIsNone(cmd.return_code)
        self.assertIsNone(cmd.stderr)
        self.assertIsNone(cmd.stdout)

        with self.assertRaises(NotImplementedError):
            cmd.execute('input')
        self.check_commands_common(cmd)

        self.assertFalse(cmd.is_exit())

    def test_declare(self):
        with self.assertRaises(ValueError):
            DeclareCommand([])
        with self.assertRaises(ValueError):
            DeclareCommand(['1', '2', '3'])
        with self.assertRaises(ValueError):
            DeclareCommand(['1'])
        with self.assertRaises(ValueError):
            DeclareCommand(['1'] * 15)

        var = 'var'
        val1 = 'val1'
        val2 = 'val2'
        val3 = 'val3'

        class Memory:
            def __init__(self):
                self.d = {}

            def set_value(self, variable, value):
                self.d[variable] = value

        mem = Memory()

        for i, val in enumerate([val1, val2, val3]):
            cmd = DeclareCommand([var, val])
            cmd.execute(f'input{i}', mem)
            self.assertEqual(mem.d[var], val)
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)
            self.assertEqual(cmd.get_stdout(), '')
            self.assertEqual(cmd.get_stderr(), '')

    @staticmethod
    def create_file(name, content):
        with open(name, 'wb') as f:
            f.write(content)

    @staticmethod
    def remove_file(name):
        os.remove(name)

    def test_file_reading(self):
        fn1 = 'file1'
        content1 = b'text content'
        fn2 = 'file2'
        content2 = b'\n\a\0\xd0\xa9\x70'
        fn3 = 'file3'
        content3 = b''

        for fn, content in [(fn1, content1), (fn2, content2), (fn3, content3)]:
            self.create_file(fn, content)
            bs, stderr, return_code = get_file_bytes(fn, '')
            self.assertEqual(bs, content)
            self.assertEqual(stderr, '')
            self.assertEqual(return_code, SUCCESS_RETURN_CODE)

        for fn in [fn1, fn2, fn3]:
            self.remove_file(fn)

        bs, stderr, return_code = get_file_bytes('no_such_file', '')
        self.assertEqual(bs, b'')
        self.assertEqual(return_code, FAILED_FILE_OPEN_RETURN_CODE)

        direct = 'new_directory'
        os.mkdir(direct)
        bs, stderr, return_code = get_file_bytes(direct, '')
        self.assertEqual(bs, b'')
        self.assertEqual(return_code, FAILED_FILE_OPEN_RETURN_CODE)
        os.rmdir(direct)

    def test_cat(self):
        fn1 = 'file1'
        content1 = b'text content'
        fn2 = 'file2'
        content2 = b'\n\a\0\xd0\xa9\x70'
        fn3 = 'file3'
        content3 = b''

        for content in [content1, content2, content3]:
            cmd = CatCommand([])
            self.check_commands_common(cmd)
            cmd.execute(content.decode('utf-8'))
            self.assertEqual(cmd.get_stdout(), content.decode('utf-8'))
            self.assertEqual(cmd.get_stderr(), '')
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        for i, (fn, content) in enumerate([(fn1, content1), (fn2, content2), (fn3, content3)]):
            self.create_file(fn, content)
            cmd = CatCommand([fn, f'f{i}', f'f{i + 1}'])

            self.check_commands_common(cmd)

            cmd.execute(f'input{i}')
            self.assertEqual(cmd.get_stdout(), content.decode('utf-8'))
            self.assertEqual(cmd.get_stderr(), '')
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        for fn in [fn1, fn2, fn3]:
            self.remove_file(fn)

        no_file = 'no_such_file'
        cmd = CatCommand([no_file])
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), '')
        self.assertEqual(cmd.get_return_code(), FAILED_FILE_OPEN_RETURN_CODE)

        direct = 'new_directory'
        os.mkdir(direct)
        cmd = CatCommand([direct])
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), '')
        self.assertEqual(cmd.get_return_code(), FAILED_FILE_OPEN_RETURN_CODE)
        os.rmdir(direct)

    def test_echo(self):
        content1 = 'some string'
        content2 = 'word'
        content3 = 'here three words'
        content4 = ''

        for i, content in enumerate([content1, content2, content3, content4]):
            cmd = EchoCommand(content.split())
            self.check_commands_common(cmd)
            cmd.execute(f'input{i}')
            self.assertEqual(cmd.get_stdout(), content)
            self.assertEqual(cmd.get_stderr(), '')
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

    def test_wc(self):
        fn1 = 'file1'
        content1 = b'text content'
        ans1 = '{:6d} {:6d} {:6d}'.format(1, 2, len(content1))
        fn2 = 'file2'
        content2 = b'\n\xd0\x91\xd0\xb9'
        ans2 = '{:6d} {:6d} {:6d}'.format(2, 1, len(content2))
        fn3 = 'file3'
        content3 = b''
        ans3 = '{:6d} {:6d} {:6d}'.format(0, 0, 0)
        fn4 = 'file4'
        content4 = b'\na\tb\nc\n\nd'
        ans4 = '{:6d} {:6d} {:6d}'.format(5, 4, len(content4))

        for content, ans in [(content1, ans1), (content2, ans2), (content3, ans3), (content4, ans4)]:
            cmd = WcCommand([])
            self.check_commands_common(cmd)
            cmd.execute(content.decode('utf-8'))
            self.assertEqual(cmd.get_stdout(), ans)
            self.assertEqual(cmd.get_stderr(), '')
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        for i, (fn, content, ans) in enumerate([(fn1, content1, ans1), (fn2, content2, ans2),
                                           (fn3, content3, ans3), (fn4, content4, ans4)]):
            self.create_file(fn, content)
            cmd = WcCommand([fn, f'f{i}', f'f{i + 1}'])

            self.check_commands_common(cmd)

            cmd.execute(f'input{i}')
            self.assertEqual(cmd.get_stdout(), ans)
            self.assertEqual(cmd.get_stderr(), '')
            self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        for fn in [fn1, fn2, fn3, fn4]:
            self.remove_file(fn)

        no_file = 'no_such_file'
        cmd = WcCommand([no_file])
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), '')
        self.assertEqual(cmd.get_return_code(), FAILED_FILE_OPEN_RETURN_CODE)

        direct = 'new_directory'
        os.mkdir(direct)
        cmd = WcCommand([direct])
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), '')
        self.assertEqual(cmd.get_return_code(), FAILED_FILE_OPEN_RETURN_CODE)
        os.rmdir(direct)

    def test_pwd(self):
        cmd = PwdCommand(['arg1', 'arg2'])
        self.check_commands_common(cmd)
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), os.getcwd())
        self.assertEqual(cmd.get_stderr(), '')
        self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

    def test_exit(self):
        cmd = ExitCommand(['arg1', 'arg2'])
        self.check_commands_common(cmd)
        cmd.execute('some input')
        self.assertEqual(cmd.get_stdout(), '')
        self.assertEqual(cmd.get_stderr(), '')
        self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

    def test_outer_commands(self):
        with self.assertRaises(ValueError):
            OtherCommand([])

        class Memory:
            def __init__(self):
                self.d = os.environ

            def get_env(self):
                return self.d

        mem = Memory()

        cmd = OtherCommand(['echo', 'hello', 'world'])
        self.check_commands_common(cmd)
        with self.assertRaises(ValueError):
            cmd.execute('')
        cmd.execute('!', mem)
        if os.name == 'nt':
            self.assertEqual(cmd.get_stdout(), 'hello world !' + os.linesep)
        self.assertEqual(cmd.get_stderr(), '')
        self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        new_dir = 'new_dir'

        cmd = OtherCommand(['md' if os.name == 'nt' else 'mkdir', new_dir])
        self.check_commands_common(cmd)
        cmd.execute('', mem)
        self.assertTrue(os.path.exists(new_dir))
        self.assertEqual(cmd.get_stderr(), '')
        self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)

        cmd = OtherCommand(['rmdir', new_dir] if os.name == 'nt' else ['rm', '-rf', new_dir])
        self.check_commands_common(cmd)
        cmd.execute('', mem)
        self.assertFalse(os.path.exists('new_dir'))
        self.assertEqual(cmd.get_stderr(), '')
        self.assertEqual(cmd.get_return_code(), SUCCESS_RETURN_CODE)
