import os
import sys
import unittest

from .app import MainApp


def format_out(out, err):
    correct = '>>> '
    if out != '':
        correct += f'stdout: {out}\n'
    if err != '':
        correct += f'stderr: {err}\n'
    return correct


class TestApp(unittest.TestCase):
    def run_pipe(self, user_input, expected_output):

        app = MainApp()

        in_file_name = 'testing_input_file.txt'
        out_file_name = 'testing_output_file.txt'

        inp = '\n'.join(user_input)

        with open(in_file_name, 'w') as f:
            f.write(inp)
        default_out = sys.stdout
        with open(in_file_name, 'r') as f_in:
            sys.stdin = f_in
            with open(out_file_name, 'w') as f_out:
                f_out.write('')
                sys.stdout = f_out

                app.start()
        sys.stdout = default_out
        with open(out_file_name, 'r') as f:
            content = f.read()
            self.assertEqual(content, expected_output)

        os.remove(in_file_name)
        os.remove(out_file_name)

    def test_exit(self):
        inp = ['exit']
        out = format_out('', '')
        self.run_pipe(inp, out)

    def test_echo(self):
        inp = ['echo "Some text"', 'exit']
        out = ''.join([
            format_out('Some text', ''),
            format_out('', ''),
        ])
        self.run_pipe(inp, out)

    def test_env_vars(self):
        if os.name != 'nt':
            inp = ['echo "$USER $HOME"', 'exit']
            out = ''.join([
                format_out(f'{os.environ["USER"]} {os.environ["HOME"]}', ''),
                format_out('', ''),
            ])
            self.run_pipe(inp, out)
        else:
            inp = ['echo "$WINDIR"', 'exit']
            out = ''.join([
                format_out(f'{os.environ["WINDIR"]}', ''),
                format_out('', ''),
            ])
            self.run_pipe(inp, out)

    def test_variable_assign(self):
        var = 'my_cool_variable_which_is_not_in_system'
        inp = [f'echo "${var}"', f'{var}=10', f'echo "${var}"', 'exit']

        out = ''.join([
            format_out('', ''),
            format_out('', ''),
            format_out('10', ''),
            format_out('', ''),
        ])
        self.run_pipe(inp, out)

    def test_invalid_definition(self):
        inputs = ['x=', '=10', '=', '"x y"=10', 'x y=10', 'x = 10 13', '= =', 'x y == 1', 'x y == 1 2', 'x == 1 2', '\\\\ = 1']
        outputs = [
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable value, line 1, col 1\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name, line 1, col 0\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name and value, line 1, col 0\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, incorrect variable name "x y", line 1, col 5\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, one variable name was expected, line 1, col 3\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, one value was expected, line 1, col 2\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name and value, line 1, col 2\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name, line 1, col 5\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name, line 1, col 5\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, missing variable name, line 1, col 3\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect declaration, incorrect variable name "\\", line 1, col 3\n>>> ']
        for inp, out in zip(inputs, outputs):
            self.run_pipe([inp, 'exit'], out)

    def test_invalid_input(self):
        inputs = ['\'', '"', 'a \'', 'a \"', 'a "arg1" "\'arg2\'" \'']
        outputs = [
            '>>> stderr: Failed to substitute variables: Uncovered quote: col 0\n>>> ',
            '>>> stderr: Failed to substitute variables: Uncovered quote: col 0\n>>> ',
            '>>> stderr: Failed to substitute variables: Uncovered quote: col 2\n>>> ',
            '>>> stderr: Failed to substitute variables: Uncovered quote: col 2\n>>> ',
            '>>> stderr: Failed to substitute variables: Uncovered quote: col 18\n>>> ']
        for inp, out in zip(inputs, outputs):
            self.run_pipe([inp, 'exit'], out)

    def test_invalid_input_pipe(self):
        inputs = ['x = a | | echo 1', '| x = a', 'x = a | ', 'x = a ||', 'x = a |||', '|', '|x = a|']
        outputs = [
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 8\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 0\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 6\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 7\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 8\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 0\n>>> ',
            '>>> stderr: Failed to parse input: Incorrect pipeline, expected function call or variable declaration, line 1, col 6\n>>> '
        ]
        for inp, out in zip(inputs, outputs):
            self.run_pipe([inp, 'exit'], out)

    def test_quotes(self):
        var_name = 'var_name'
        inp = [
            f'{var_name}=10',
            f'echo "{var_name}=${var_name}"',
            f'echo \'{var_name}=${var_name}\'',
            f'echo "\'{var_name}=${var_name}\'"',
            f'echo \'"{var_name}=${var_name}"\'',
            'exit'
        ]
        out = ''.join([
            format_out('', ''),
            format_out(f'{var_name}=10', ''),
            format_out(f'{var_name}=${var_name}', ''),
            format_out(f'\'{var_name}=10\'', ''),
            format_out(f'"{var_name}=${var_name}"', ''),
            format_out('', ''),
        ])
        self.run_pipe(inp, out)


if __name__ == '__main__':
    unittest.main()
