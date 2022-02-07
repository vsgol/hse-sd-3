"""Responsible for substituting variables into the input string"""

import re
from string import Template

from CLI.src.memory import Memory


def substitute(input_string: str, memory: Memory) -> str:
    """
    selects substrings in quotes in the input string and substitutes variables if they are not in single quotes

    :param input_string: String for conversion
    :param memory: Environment variables
    :return: Substitution result
    """

    pattern = re.compile("""((\\\.)|[^"'\\\])+|("((\\\.)|[^"])*")|('((\\\.)|[^'\\\])*')""")
    pos = 0
    res = []
    for substring in pattern.finditer(input_string):
        new_pos = pos + len(substring[0])
        if substring[0] != "'":
            try:
                substring = Template(substring[0]).substitute(memory.get_env())
            except ValueError as err:
                print(f'ValueError {err!s}')
            except KeyError as err:
                print(f'KeyError {err!s}')
        res.append(substring)
        pos = new_pos
    return ''.join(res)
