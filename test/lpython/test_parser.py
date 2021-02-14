import io
import pytest  # noqa

from lpython.tokeniser import Lex
from lpython.parser import Parser


def parse(code):
    lexer = Lex(io.StringIO(code))
    parser = Parser(lexer)

    while not parser.eof:
        print(parser.parse(), end='')


def test_simple(capfd):
    parse("print(\"X\")")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "print(\"X\")")
    assert(not err)


def test_multiple(capfd):
    parse("print(\"X\") print(\"Y\")")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "print(\"X\") print(\"Y\")")
    assert(not err)


def test_multiple_semi(capfd):
    parse("print(\"X\"); print(\"Y\")")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "print(\"X\")\nprint(\"Y\")")
    assert(not err)


def test_scope_empty(capfd):
    parse("if X:")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:")
    assert("input ended but there were unclosed block" in err)


def test_scope_unclosed(capfd):
    parse("if X: print()")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()")
    assert("input ended but there were unclosed block" in err)


def test_scope_good(capfd):
    parse("if X: print(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()")
    assert(not err)


def test_scope_wrongclose(capfd):
    parse("if X: print(); endwith")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()")
    assert("last opened block 'if' closed" in err)


def test_multi_scope_empty(capfd):
    parse("if X: if Y:")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    if Y:")
    assert("input ended but there were unclosed block" in err)


def test_multi_scope_unclosed_both(capfd):
    parse("if X: print(); if Y: print()")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()\n    if Y:\n        print()")
    assert("input ended but there were unclosed block" in err)


def test_multi_scope_unclosed_one(capfd):
    parse("if X: print(); if Y: print(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()\n    if Y:\n        print()")
    assert("input ended but there were unclosed block" in err)


def test_multi_scope_good(capfd):
    parse("if X: print(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()")
    assert(not err)


def test_multi_scope_wrongclose(capfd):
    parse("if X: print(); if Y: print(); endwith")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()\n    if Y:\n        print()")
    assert("last opened block 'if' closed" in err)


def test_multi_scope_different_good(capfd):
    parse("if X: print(); with Y: print(); endwith; endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()\n    with Y:\n        print()")
    assert(not err)


def test_multi_scope_different_swapclose(capfd):
    parse("if X: print(); with Y: print(); endif; endwith")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    print()\n    with Y:\n        print()")
    assert("last opened block 'with' closed by endif" in err)
