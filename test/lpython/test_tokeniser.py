import io

from lpython.tokeniser import Lex, TokenKind, EOF_MAGIC, NONE


def lex(code):
    lexer = Lex(io.StringIO(code))
    tok = NONE
    tokens = []

    while True:
        tok = lexer.next()
        if tok.kind == TokenKind.EOF:
            break
        if tok == NONE:
            continue
        tokens.append(tok)

    return tokens


def toks(code):
    return list(map(lambda tok: tok.kind, lex(code)))


def test_simple_words():
    assert(toks("") == [])
    assert(toks("import json") == [TokenKind.UNINTERESTING,
                                   TokenKind.UNINTERESTING])
    assert(toks("import json; import time;") == [TokenKind.UNINTERESTING,
                                                 TokenKind.UNINTERESTING,
                                                 TokenKind.SEMI,
                                                 TokenKind.UNINTERESTING,
                                                 TokenKind.UNINTERESTING,
                                                 TokenKind.SEMI])


def test_keywords():
    assert(toks("if X:") == [TokenKind.IF,
                             TokenKind.UNINTERESTING,
                             TokenKind.COLON])

    assert(toks("ifIam") == [TokenKind.UNINTERESTING])


def test_assignment():
    asg = lex("myVar = value;")
    assert(len(asg) == 4)
    assert(asg[0].kind == TokenKind.UNINTERESTING and
           asg[0].value == "myVar " and
           asg[0].position == 0)
    assert(asg[1].kind == TokenKind.UNINTERESTING and
           asg[1].value == "= " and
           asg[1].position == 6)
    assert(asg[2].kind == TokenKind.UNINTERESTING and
           asg[2].value == "value" and
           asg[2].position == 8)
    assert(asg[3].kind == TokenKind.SEMI and asg[3].value == ";" and
           asg[3].position == 13)


def test_parens():
    assert(toks("if foo(bar):") == [TokenKind.IF,
                                    TokenKind.UNINTERESTING,
                                    TokenKind.OPEN,
                                    TokenKind.UNINTERESTING,
                                    TokenKind.CLOSE,
                                    TokenKind.COLON])


def test_eof():
    empty = io.StringIO("")
    eof = Lex(empty).next()
    assert(empty.getvalue() == EOF_MAGIC)
    assert(eof.kind == TokenKind.EOF and eof.position == 0)
