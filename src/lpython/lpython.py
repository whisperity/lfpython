import io
import sys

from .parser import Parser
from .tokeniser import Lex


def transpile(codeStream):
    """Rewrites the input stream of program code according to LPython rules."""
    lexer = Lex(codeStream)
    parser = Parser(lexer)

    while not parser.eof:
        stmt = parser.parse()
        print(stmt, end='')


transpile(io.StringIO(" ".join(sys.argv[1:])))
