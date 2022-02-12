import random
import unittest

from .lexer import IllegalCharacter
from .parser import Parser, IncompleteToken


class MyTestCase(unittest.TestCase):
    correct_var_names = ['_', 'v', 'val1', 'val_2', 'v_a_l_3__', 'vAl_4', 'v5al5', 'VAL_6', 'V7', '_8']
    correct_fun_names = correct_var_names + ['echo', 'pwd', 'cat', 'wc', 'exit', 'Get-Content', 'fun-nAme2_4']
    command_names = ['echo', 'pwd', 'cat', 'wc', 'exit']
    correct_values = ['value1', '\'value2\'', '\"test3\"', """'te st 4'""", '''"te s t5"''',
                      '''"te\\\\st 6 \\""''', """'te\\\\st 7 \\"'"""]
    formatted_values = ['value1', 'value2', 'test3', """te st 4""", '''te s t5''',
                        '''te\\st 6 "''', '''te\\\\st 7 \\"''']

    incorrect_fun_names = ['fu\'n', 'fu\"n']
    incorrect_var_names = incorrect_fun_names + ['1', '1var', '-var', 'var-', 'va-r', 'var>', 'va\\r']

    parser = Parser()

    def test_declaration(self):
        def check_correct(input_str, variable, value):
            res = self.parser.parse(input_str)
            self.assertEqual(1, len(res))
            self.assertEqual(variable, res[0].variable)
            self.assertEqual(value, res[0].value)

        def check_incorrect(input_str, exception):
            with self.assertRaises(exception):
                self.parser.parse(input_str)

        for var_name in self.correct_var_names:
            check_correct(var_name + ' = a', var_name, 'a')
        for val, formatted_val in zip(self.correct_values, self.formatted_values):
            check_correct('var = ' + val, 'var', formatted_val)
        for input_str in ['a=b', 'a\t \t = \t\n b \t ', 'a \n\n=b', '\n \n \t a  =b']:
            check_correct(input_str, 'a', 'b')

        for var_name in self.incorrect_var_names:
            check_incorrect(var_name + ' = a', (IllegalCharacter, IncompleteToken))
        check_incorrect('a = b, c', IncompleteToken)
        check_incorrect('a = ', IncompleteToken)
        check_incorrect('a b = c', IncompleteToken)

    def test_function_call(self):
        def check_correct(input_str, other_fun_name, args):
            res = self.parser.parse(input_str)
            self.assertEqual(1, len(res))
            if other_fun_name is not None:
                self.assertEqual(other_fun_name, res[0].args[0])
                self.assertEqual(args, res[0].args[1:])

        def check_incorrect(input_str, exception):
            with self.assertRaises(exception):
                self.parser.parse(input_str)

        for fun_name in self.correct_fun_names:
            check_correct(fun_name, fun_name if fun_name not in self.command_names else None, [])
        for arg, formatted_arg in zip(self.correct_values, self.formatted_values):
            check_correct('fun ' + arg, 'fun', [formatted_arg])
        for input_str in ['a b', 'a\t \t  \t\n b \t ', 'a \n\nb', '\n \n \t a  b']:
            check_correct(input_str, 'a', ['b'])

        for fun_name in self.correct_fun_names:
            args_pos = random.sample(range(len(self.correct_values)), 4)
            args = [self.correct_values[i] for i in args_pos]
            formatted_args = [self.formatted_values[i] for i in args_pos]
            check_correct(fun_name + ' ' + ' '.join(args),
                          fun_name if fun_name not in self.command_names else None,
                          formatted_args)

        for fun_name in self.incorrect_fun_names:
            check_incorrect(fun_name + ' a', (IllegalCharacter, IncompleteToken))


if __name__ == '__main__':
    unittest.main()
