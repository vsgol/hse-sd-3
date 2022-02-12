"""Responsible for substituting variables into the input string"""

import re
from string import Template

from CLI.cli_module.memory import Memory


def substitute(input_string: str, memory: Memory) -> str:
    """Selects substrings in quotes in the input string and substitutes variables if they are not in single quotes

    args:
        input_string (str): String for conversion
        memory (Memory): Environment variables

    returns:
        str: substitution result
    """

    pattern = re.compile("""((\\\.)|[^"'\\\])+|("((\\\.)|[^"])*")|('((\\\.)|[^'\\\])*')""")
    col = 0
    res = []
    for matching in pattern.finditer(input_string):
        if col != matching.start():
            raise ValueError(f'Uncovered quote: col {col}')
        new_col = col + len(matching[0])
        if matching[0][0] != "'":
            try:
                matching = Template(matching[0]).substitute(memory)
            except ValueError as err:
                matching = re.match(
                    'Invalid placeholder in string: line (?P<line_num>[-+]?\d+), col (?P<col_num>[-+]?\d+)',
                    err.args[0])
                raise ValueError('Invalid placeholder in string: col {}'.format(int(matching.group('col_num')) + col))
        else:
            matching = matching[0]
        res.append(matching)
        col = new_col
    if col != len(input_string):
        raise ValueError(f'Uncovered quote: col {col}')
    return ''.join(res)
