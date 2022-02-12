import re
from typing import List

import ply.yacc as yacc

from .command import CommandFactory, Command
from .lexer import Lexer, IllegalCharacter


class IncompleteToken(Exception):
    def __init__(self, value, line=None, col=None):
        self.value = value
        self.line = line
        self.col = col

    def __str__(self):
        if self.line is not None:
            return "{!s}, line {}, col {}".format(self.value, self.line, self.col)
        else:
            return "{!s}".format(self.value)


class Parser:
    """Responsible for the parser's grammar

    methods:
        parse: splits the input string into commands
    """

    def __init__(self):
        self.lexer = Lexer()
        self.parser = make_parser(self)
        self.factory = CommandFactory()

    tokens = Lexer.tokens

    # ==> Defining the context-free grammar specifications
    def p_declaration(self, p):
        """declaration : EQUAL
                       | EQUAL declaration
                       | EQUAL value_sequence
                       | value_sequence EQUAL
                       | value_sequence EQUAL declaration
                       | value_sequence EQUAL value_sequence"""
        # Only the last option is correct declaration, if both value_sequences have one value
        if len(p) == 2:
            if p[1] == '=':
                raise IncompleteToken(f'Incorrect declaration, missing variable name and value',
                                      p.slice[1].lineno, p.slice[1].lexpos)
        elif len(p) == 3:
            if p[1] == '=':
                raise IncompleteToken(f'Incorrect declaration, missing variable name',
                                      p.slice[1].lineno, p.slice[1].lexpos)
            elif p[2] == '=':
                raise IncompleteToken(f'Incorrect declaration, missing variable value',
                                      p.slice[2].lineno, p.slice[2].lexpos)
        elif len(p) == 4:
            if p.slice[3].type == 'definition':
                raise IncompleteToken(f'Incorrect declaration, one sign equal was expected',
                                      p.slice[2].lineno, p.slice[2].lexpos)
            elif len(p[1]) > 1:
                raise IncompleteToken(f'Incorrect declaration, one variable name was expected',
                                      p.slice[2].lineno, p.slice[2].lexpos)
            elif len(p[3]) > 1:
                raise IncompleteToken(f'Incorrect declaration, one value was expected',
                                      p.slice[2].lineno, p.slice[2].lexpos)
            elif re.fullmatch('[_a-z][_a-z0-9]*', p[1][0], re.IGNORECASE) is None:
                raise IllegalCharacter(f'Incorrect declaration, incorrect variable name "{p[1][0]}"',
                                       p.slice[2].lineno, p.slice[2].lexpos)
            else:
                p[0] = self.factory.build_declare_command(p[1][0], p[3][0])

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
        """function_call : value_sequence"""
        p[0] = self.factory.tokens_to_commands(p[1][0], p[1][1:])

    def p_command(self, p):
        """command : declaration
                   | function_call"""
        p[0] = p[1]

    def p_pipeline(self, p):
        """pipeline : command
                    | PIPE
                    | PIPE pipeline
                    | command PIPE
                    | command PIPE pipeline"""
        # first and last options are correct pipelines
        if len(p) == 2:
            if p[1] == '|':
                raise IncompleteToken(f'Incorrect pipeline, expected function call or variable declaration',
                                      p.slice[1].lineno, p.slice[1].lexpos)
            else:
                p[0] = [p[1]]
        elif len(p) == 3:
            if p[1] == '|':
                raise IncompleteToken(f'Incorrect pipeline, expected function call or variable declaration',
                                      p.slice[1].lineno, p.slice[1].lexpos)
            elif p[2] == '|':
                raise IncompleteToken(f'Incorrect pipeline, expected function call or variable declaration',
                                      p.slice[2].lineno, p.slice[2].lexpos)
        elif len(p) == 4:
            p[0] = [p[1]].extend(p[3])

    # Error rule for parsing errors
    def p_error(self, p):
        raise IncompleteToken(p)

    def parse(self, code: str) -> List[Command]:
        """Splits the input string into commands
        
        args:
            code (str): input string to split

        returns:
            List [Command]: sequence of pipeline commands
        """
        return self.parser.parse(code, self.lexer)


def make_parser(mod):
    return yacc.yacc(module=mod,
                     debug=False,
                     write_tables=False,
                     start='pipeline')
