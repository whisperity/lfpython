# Copyright (C) 2020 Whisperity
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import pytest  # noqa

from py_singleline.tokeniser import Lex
from py_singleline.parser import Parser


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


def test_ifelse(capfd):
    parse("if X: a(); else: b(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    a()\n    \nelse :\n    b()")
    assert(not err)


def test_else(capfd):
    parse("else: b(); endif")
    out, err = capfd.readouterr()
    assert("'else' encountered but no previous 'if'" in err)


def test_elif(capfd):
    parse("elif X: a(); endif")
    out, err = capfd.readouterr()
    assert("'elif' encountered but no previous 'if'" in err)


def test_whileelse(capfd):
    parse("while X: a(); else Y: b(); endif; endwhile")
    out, err = capfd.readouterr()
    assert("'else' encountered but no previous 'if'" in err)


def test_ifelif(capfd):
    parse("if X: a(); elif Y: b(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    a()\n    \nelif Y:\n    b()")
    assert(not err)


def test_ifelif_multi(capfd):
    parse("if X: a(); elif Y: b(); elif Z: c(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() == "if X:\n    a()\n    \n"
                           "elif Y:\n    b()\n    \n"
                           "elif Z:\n    c()")
    assert(not err)


def test_ifelifelse(capfd):
    parse("if X: print(); elif Y: print(); else: print(); endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() ==
           "if X:\n    print()\n    \n"
           "elif Y:\n    print()\n    \n"
           "else :\n    print()")
    assert(not err)


def test_ifelifelifelse(capfd):
    parse("if X: print(); "
          "elif Y: print(); "
          "elif Z: print(); "
          "else: print(); "
          "endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() ==
           "if X:\n    print()\n    \n"
           "elif Y:\n    print()\n    \n"
           "elif Z:\n    print()\n    \n"
           "else :\n    print()")
    assert(not err)


def test_nested_if(capfd):
    parse("if X: x(); "
          "if Y: y(); "
          "elif Yb: yb(); "
          "endif; "
          "elif Xb: xb(); "
          "else: xe(); "
          "endif")
    out, err = capfd.readouterr()
    assert(out.rstrip() ==
           "if X:\n"
           "    x()\n"
           "    if Y:\n"
           "        y()\n"
           "        \n"
           "    elif Yb:\n"
           "        yb()\n"
           "        \n"
           "    \n"
           "elif Xb:\n"
           "    xb()\n"
           "    \n"
           "else :\n"
           "    xe()")
    assert(not err)
