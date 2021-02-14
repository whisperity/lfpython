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
    assert(toks("import json") == [TokenKind.VERBATIM,
                                   TokenKind.VERBATIM])
    assert(toks("import json; import time;") == [TokenKind.VERBATIM,
                                                 TokenKind.VERBATIM,
                                                 TokenKind.SEMI,
                                                 TokenKind.VERBATIM,
                                                 TokenKind.VERBATIM,
                                                 TokenKind.SEMI])


def test_keywords():
    assert(toks("if X:") == [TokenKind.IF,
                             TokenKind.VERBATIM,
                             TokenKind.COLON])

    assert(toks("ifIam") == [TokenKind.VERBATIM])


def test_assignment():
    asg = lex("myVar = value;")
    assert(len(asg) == 4)
    assert(asg[0].kind == TokenKind.VERBATIM and
           asg[0].value == "myVar " and
           asg[0].position == 0)
    assert(asg[1].kind == TokenKind.VERBATIM and
           asg[1].value == "= " and
           asg[1].position == 6)
    assert(asg[2].kind == TokenKind.VERBATIM and
           asg[2].value == "value" and
           asg[2].position == 8)
    assert(asg[3].kind == TokenKind.SEMI and asg[3].value == ";" and
           asg[3].position == 13)


def test_parens():
    assert(toks("if foo(bar):") == [TokenKind.IF,
                                    TokenKind.VERBATIM,
                                    TokenKind.OPEN,
                                    TokenKind.VERBATIM,
                                    TokenKind.CLOSE,
                                    TokenKind.COLON])


def test_string_concat():
    assert(toks("input(\"Foo\" + x + \":\");") == [
        TokenKind.VERBATIM,  # input
        TokenKind.OPEN,      # (
        TokenKind.VERBATIM,  # "Foo" (+ ws)
        TokenKind.VERBATIM,  # +     (+ ws)
        TokenKind.VERBATIM,  # x     (+ ws)
        TokenKind.VERBATIM,  # +     (+ ws)
        TokenKind.VERBATIM,  # ":"
        TokenKind.CLOSE,     # )
        TokenKind.SEMI       # ;
        ])


def test_eof():
    empty = io.StringIO("")
    eof = Lex(empty).next()
    assert(empty.getvalue() == EOF_MAGIC)
    assert(eof.kind == TokenKind.EOF and eof.position == 0)


def test_special_in_string():
    assert(toks("sp = xxx.split(\"/\")") == [TokenKind.VERBATIM,  # sp
                                             TokenKind.VERBATIM,  # =
                                             TokenKind.VERBATIM,  # xxx.split
                                             TokenKind.OPEN,      # (
                                             TokenKind.VERBATIM,  # "/"
                                             TokenKind.CLOSE      # )
                                             ])


def test_colon_in_string():
    assert(toks("X = \"if Y: z()\"") == [TokenKind.VERBATIM,  # X
                                         TokenKind.VERBATIM,  # =
                                         TokenKind.VERBATIM,  # "if Y: z()"
                                         ])


def test_nested_strings():
    input_text = """
X = foo();
Y = "bar";
Z = 'baz';
A = "if 'foo' is not None: qux()";
"""
    assert(toks(input_text) == [TokenKind.VERBATIM,  # X
                                TokenKind.VERBATIM,  # =
                                TokenKind.VERBATIM,  # foo
                                TokenKind.OPEN,      # (
                                TokenKind.CLOSE,     # )
                                TokenKind.SEMI,      # ;

                                TokenKind.VERBATIM,  # Y
                                TokenKind.VERBATIM,  # =
                                TokenKind.VERBATIM,  # "bar"
                                TokenKind.SEMI,      # ;

                                TokenKind.VERBATIM,  # Z
                                TokenKind.VERBATIM,  # =
                                TokenKind.VERBATIM,  # 'baz'
                                TokenKind.SEMI,      # ;

                                TokenKind.VERBATIM,  # A
                                TokenKind.VERBATIM,  # =
                                # "if 'foo' is not None: qux()"
                                TokenKind.VERBATIM,
                                TokenKind.SEMI       # ;
                                ])

    tokv = lex(input_text)
    assert(len(tokv) == 18)
    assert(tokv[8].value == "\"bar\"")
    assert(tokv[12].value == "\'baz\'")
    assert(tokv[16].value == "\"if 'foo' is not None: qux()\"")
