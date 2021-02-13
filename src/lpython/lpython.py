import io
import pprint
import sys

from .tokeniser import Lex, Token, TokenKind


def transpile(codeStream):
    """Rewrites the input stream of program code according to LPython rules."""
    output = io.StringIO()

    lexer = Lex(codeStream)
    while True:
        tok = lexer.next()
        if tok.kind == TokenKind.NONE:
            continue
        pprint.pprint(tok.__dict__)
        if tok.kind == TokenKind.EOF:
            break


transpile(io.StringIO(" ".join(sys.argv[1:])))
