import unittest

from CLI.cli_module.memory import Memory
from .formatter import substitute


class MyTestCase(unittest.TestCase):
    correct_var_names = ['v', 'val1', 'val_2', 'v_a_l_3__', 'vAl_4', 'v5al5', 'VAL_6', 'V7', '_8']
    incorrect_var_names = ['1', '1var', '-var', '<var>', '\\var']

    class TestMemory(Memory):
        def __init__(self, test_case, current_vars):
            super().__init__()
            self.test_case = test_case
            self.current_vars = current_vars

        def get_value(self, key):
            self.test_case.assertIn(key, self.current_vars)
            return super().get_value(key)

    def test_substitute(self):
        current_vars = []
        test_memory = self.TestMemory(self, current_vars)
        for var_name in self.correct_var_names:
            current_vars.append(var_name)
            res = substitute(f'test substitute var = ${var_name}', test_memory)
            self.assertEqual('test substitute var = ', res)

            test_memory[var_name] = 'test_val'
            res = substitute(f'test substitute var = ${var_name}', test_memory)
            self.assertEqual('test substitute var = test_val', res)
            current_vars.remove(var_name)

        for var_name in self.incorrect_var_names:
            with self.assertRaises(ValueError):
                substitute(f'test substitute var = ${var_name}', test_memory)

        var_names = ['$var1', '$var2', '$var3', '$var4']
        var_values = [1, 'val', '\n\t\\\"\', test', '']
        test_str = 'test1 var1 = {0}, test2 var2={1}, test3 var3\t\t=\t{2}, test4 var4\n=\n{3}'
        for var_name, var_value in zip(var_names, var_values):
            test_memory[var_name[1:]] = var_value
            current_vars.append(var_name[1:])
        res = substitute(test_str.format(*var_names), test_memory)
        self.assertEqual(test_str.format(*var_values), res)
        current_vars.clear()

        self.assertEqual('$', substitute('$$', test_memory))

    def test_quotes(self):
        current_vars = []
        test_memory = self.TestMemory(self, current_vars)
        for var_name in self.correct_var_names:
            current_vars.append(var_name)
            test_memory[var_name] = 'test_val'
            res = substitute(f'''test substitute var = ${var_name} ''', test_memory)
            self.assertEqual('''test substitute var = test_val ''', res)
            res = substitute(f'''test substitute var = "${var_name}" ''', test_memory)
            self.assertEqual('''test substitute var = "test_val" ''', res)
            res = substitute(f'''test substitute var = '${var_name}' ''', test_memory)
            self.assertEqual(f'''test substitute var = '${var_name}' ''', res)

            res = substitute(f'''test substitute var = \\"${var_name}\\" ''', test_memory)
            self.assertEqual(f'''test substitute var = \\"test_val\\" ''', res)
            res = substitute(f'''test substitute var = \\'${var_name}\\' ''', test_memory)
            self.assertEqual(f'''test substitute var = \\'test_val\\' ''', res)
            res = substitute(f'''test substitute var = $${var_name} ''', test_memory)
            self.assertEqual(f'''test substitute var = ${var_name} ''', res)

            res = substitute(f'''test substitute var = "'${var_name}'" ''', test_memory)
            self.assertEqual(f'''test substitute var = "'test_val'" ''', res)
            res = substitute(f'''test substitute var = "\\"${var_name}\\"" ''', test_memory)
            self.assertEqual(f'''test substitute var = "\\"test_val\\"" ''', res)
            res = substitute(f'''test substitute var = "\\'${var_name}\\'" ''', test_memory)
            self.assertEqual(f'''test substitute var = "\\'test_val\\'" ''', res)
            res = substitute(f'''test substitute var = "$${var_name}" ''', test_memory)
            self.assertEqual(f'''test substitute var = "${var_name}" ''', res)

            res = substitute(f'''test substitute var = '"${var_name}"' ''', test_memory)
            self.assertEqual(f'''test substitute var = '"${var_name}"' ''', res)
            res = substitute(f'''test substitute var = '\\"${var_name}\\"' ''', test_memory)
            self.assertEqual(f'''test substitute var = '\\"${var_name}\\"' ''', res)
            res = substitute(f'''test substitute var = '\\'${var_name}\\'' ''', test_memory)
            self.assertEqual(f'''test substitute var = '\\'${var_name}\\'' ''', res)
            res = substitute(f'''test substitute var = '$${var_name}' ''', test_memory)
            self.assertEqual(f'''test substitute var = '$${var_name}' ''', res)

            current_vars.remove(var_name)


if __name__ == '__main__':
    unittest.main()
