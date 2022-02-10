"""Responsible for substituting variables into the input string"""

import re
from string import Template

from CLI.cli_module.memory import Memory


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
    for matching in pattern.finditer(input_string):
        new_pos = pos + len(matching[0])
        if matching[0][0] != "'":
            matching = Template(matching[0]).substitute(memory)
        else:
            matching = matching[0]
        res.append(matching)
        pos = new_pos
    return ''.join(res)
