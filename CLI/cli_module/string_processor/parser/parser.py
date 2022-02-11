import re
from typing import List

import ply.yacc as yacc

from .command import CommandFactory, Command
from .lexer import Lexer, IllegalCharacter


class IncompleteToken(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = make_parser(self)
        self.factory = CommandFactory()

    tokens = Lexer.tokens

    # ==> Defining the context-free grammar specifications
    def p_declaration(self, p):
        """declaration : STRING EQUAL value"""
        if re.fullmatch('[_a-z][_a-z0-9]*', p[1], re.IGNORECASE) is None:
            raise IllegalCharacter(f'Incorrect variable name "{p[1]}"', p.slice[1].lineno, p.slice[1].lexpos)
        p[0] = self.factory.build_declare_command(p[1], p[3])

    def p_value_sequence(self, p):
        """value_sequence : value value_sequence
                          | value"""
        p[0] = [p[1]]
        if len(p) == 3:
            p[0].extend(p[2])

    def p_value(self, p):
        """value : STRING_IN_QUOTES
                 | STRING"""
        p[0] = p[1]

    def p_function_call(self, p):
        """function_call : STRING value_sequence
                         | STRING"""
        if len(p) == 3:
            p[0] = self.factory.tokens_to_commands(p[1], p[2])
        else:
            p[0] = self.factory.tokens_to_commands(p[1], [])

    def p_command(self, p):
        """command : declaration
                   | function_call"""
        p[0] = p[1]

    def p_pipeline(self, p):
        """pipeline : command PIPE pipeline
                    | command"""
        p[0] = [p[1]]
        if len(p) == 4:
            p[0].extend(p[3])

    # Error rule for parsing errors
    def p_error(self, p):
        raise IncompleteToken(p)

    def parse(self, code: str) -> List[Command]:
        return self.parser.parse(code, self.lexer)


def make_parser(mod):
    return yacc.yacc(module=mod,
                     debug=False,
                     write_tables=False,
                     start='pipeline')
