import os
import sys
import unittest

from .app import MainApp


def format_out(out, err):
        return f'>>> stdout: {out}\nstderr:{err}'


class TestApp(unittest.TestCase):
    def run_pipe(self, user_input, expected_output):

        app = MainApp()

        in_file_name = 'testing_input_file.txt'
        out_file_name = 'testing_output_file.txt'

        inp = '\n'.join(user_input)

        with open(in_file_name, 'w') as f:
            f.write(inp)

        with open(in_file_name, 'r') as f_in:
            sys.stdin = f_in
            with open(out_file_name, 'w') as f_out:
                f_out.write('')
                sys.stdout = f_out

                app.start()

        with open(out_file_name, 'r') as f:
            content = f.read()[:-1]  # new line remove
            self.assertEqual(content, expected_output)

        os.remove(in_file_name)
        os.remove(out_file_name)

    def test_exit(self):
        inp = ['exit']
        out = format_out('', '')
        self.run_pipe(inp, out)

    def test_echo(self):
        inp = ['echo "Some text"', 'exit']
        out = '\n'.join([
            format_out('Some text', ''),
            format_out('', ''),
            ])
        self.run_pipe(inp, out)

    def test_env_vars(self):
        inp = ['echo "$USER $HOME"', 'exit']
        out = '\n'.join([
            format_out(f'{os.environ["USER"]} {os.environ["HOME"]}', ''),
            format_out('', ''),
            ])
        self.run_pipe(inp, out)

    def test_variable_assign(self):
        var = 'my_cool_variable_which_is_not_in_system'
        inp = [f'echo "${var}"', f'{var}=10', f'echo "${var}"', 'exit']
        #print(inp)
        out = '\n'.join([
            format_out('', ''),
            format_out('', ''),
            format_out('10', ''),
            format_out('', ''),
            ])
        self.run_pipe(inp, out)


if __name__ == '__main__':
    unittest.main()