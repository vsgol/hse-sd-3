import ply.yacc as yacc
from typing import List, Dict
from .lexer import Lexer

from .command import CommandFactory, Command, DeclCommand


class IncompleteToken(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(''.format(self.value))


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.memory = None
        self.parser = make_parser(self)

    tokens = Lexer.tokens

    # ==> Defining the context-free grammar specifications
    def p_declaration(self, p):
        """declaration : STRING EQUAL value"""
        p[0] = DeclCommand(p[1], p[2], self.memory)

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
            p[0] = CommandFactory.tokens_to_commands(p[1], p[2])
        else:
            p[0] = CommandFactory.tokens_to_commands(p[1], [])

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

    def parse(self, code: str, memory: Dict[str, str]) -> List[Command]:
        self.memory = memory
        return self.parser.parse(code, self.lexer)


def make_parser(mod):
    return yacc.yacc(module=mod,
                     debug=False,
                     write_tables=False,
                     start='pipeline')
