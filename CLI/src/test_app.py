import os
import sys
import unittest

from .app import MainApp


class MyTestCase(unittest.TestCase):
    def test_exit(self):

        app = MainApp()

        in_file_name = 'testing_input_file.txt'
        out_file_name = 'testing_output_file.txt'

        inp = 'exit'

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
            self.assertEqual(content, f'>>> stdout: \nstderr:')

        os.remove(in_file_name)
        os.remove(out_file_name)


if __name__ == '__main__':
    unittest.main()