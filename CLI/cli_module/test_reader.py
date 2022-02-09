import os
import sys
import unittest

from .reader import Reader


class TestReader(unittest.TestCase):
    def test_reader(self):
        inp1 = 'one line'
        inp2 = 'one line\nsecond line\n\n\n\n\tthird line'
        inp3 = 'one line\nsecond line\n\n\n\n\tthird line\n more lines    are writen \n c:'
        file_name = 'testing_input_file.txt'

        reader = Reader()
        for inp in [inp1, inp2, inp3]:
            with open(file_name, 'w') as f:
                f.write(inp)
            lines = []
            with open(file_name, 'r') as f:
                sys.stdin = f
                for i in range(len(inp.split('\n'))):
                    lines.append(reader.get_line())
            self.assertEqual(inp, '\n'.join(lines))
        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
