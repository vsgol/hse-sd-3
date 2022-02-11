import re

from ply import lex


class IllegalCharacter(Exception):
    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

    def __str__(self):
        return "{}, line {}, col {}".format(self.value, self.line, self.col)


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.lexer.linepos = 0

    def __iter__(self):
        return iter(self.lexer)

    def token(self):
        return self.lexer.token()

    def input(self, data):
        self.lexer.input(data)

    # List of token names
    tokens = [
        'STRING_IN_QUOTES',
        'STRING',
        'PIPE',
        'EQUAL'
    ]

    # --> Defining regular expression rules ---

    t_ignore = ' \t'
    t_PIPE = r'\|'
    t_EQUAL = '='
    t_STRING = r"""(\\[bfrnt"/\\]|[^=|\s"'\u005C\u0000-\u001F\u007F-\u009F]|\\u[0-9a-fA-F]{4})+"""

    @staticmethod
    def t_STRING_IN_QUOTES(t):
        r"""("((\\.)|[^\\"])*")|('((\\.)|[^\\'])*')"""
        if t.value[0] == '"':
            t.value = t.value[1:-1]
            t.value = re.subn('''\\\(?P<char>["\\\])''', '''\g<char>''', t.value)[0]
        else:
            t.value = t.value[1:-1]
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    # -----------------------------------------

    # Error rule for lexing errors
    @staticmethod
    def t_error(t):
        # The lexer stops executing and raise a LexerError
        raise IllegalCharacter(t.value[0], t.lineno, t.lexpos)

    @staticmethod
    def find_column(inp, token):
        line_start = inp.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
