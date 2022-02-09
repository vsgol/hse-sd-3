import unittest
import os

from .memory import Memory


class TestMemory(unittest.TestCase):
    def test_memory(self):
        mem = Memory()

        var1 = 'var1'
        var2 = 'var2'
        var3 = 'var3'
        val1 = 'val1'
        new_val1 = 'new_val1'
        new_val2 = 'new_val2'
        val2 = 'val2'
        val3 = 'val3'

        vars = [var1, var2, var3]
        vals = [val1, val2, val3]

        for var, val in zip(vars, vals):
            self.assertEqual(mem.get_value(var), '')
            mem.set_value(var, val)
            self.assertEqual(mem.get_value(var), val)

        self.assertEquals(mem.get_value(var1), val1)
        mem.set_value(var1, new_val1)
        self.assertEqual(mem.get_value(var1), new_val1)
        mem.set_value(var1, new_val2)
        self.assertEqual(mem.get_value(var1), new_val2)
        expected = dict(os.environ)
        expected.update({var1: new_val2, var2: val2, var3: val3})
        self.assertDictEqual(expected, mem.get_env())

if __name__ == '__main__':
    unittest.main()
