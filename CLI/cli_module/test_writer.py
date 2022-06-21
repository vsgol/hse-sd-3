import os
import sys
import unittest

from .writer import Writer


class TestWriter(unittest.TestCase):
    def test_writer(self):
        so1 = 'one line'
        se1 = 'err'
        so2 = 'one line\nsecond line\n\n\n\n\tthird line'
        se2 = 'err line\nsecond err line\n\n\tthird line errr'
        so3 = 'one line\nsecond line\n\n\n\n\tthird line\n more lines    are writen \n c:'
        se3 = 'one line\nsecond line\n\n\nerr\n\tthird line\n more lines    are writen \n c:'
        file_name = 'testing_writer_file.txt'

        writer = Writer()
        stdout = sys.stdout
        for (so, se) in [(so1, se1), (so2, se2), (so3, se3)]:
            with open(file_name, 'w') as f:
                f.write('')
                sys.stdout = f
                writer.print_outputs(so, se)
            with open(file_name, 'r') as f:
                content = f.read()[:-1]  # new line remove
                correct = ''
                if so != '':
                    correct += f'stdout: {so}\n'
                if se != '':
                    correct += f'stderr: {se}'
                self.assertEqual(content, correct)
        sys.stdout = stdout
        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
