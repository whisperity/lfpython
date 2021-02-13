import io

from lpython.tokeniser import Lex, Token, TokenKind, NONE


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
           asg[0].value == "myVar ")
    assert(asg[1].kind == TokenKind.UNINTERESTING and
           asg[1].value == "= ")
    assert(asg[2].kind == TokenKind.UNINTERESTING and
           asg[2].value == "value")
    assert(asg[3].kind == TokenKind.SEMI and asg[3].value == ";")
