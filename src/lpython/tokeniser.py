from enum import Enum


class TokenKind(Enum):
    NONE = -1
    UNINTERESTING = 0
    EOF = 1
    SEMI = 2
    COLON = 3

    IF = 8
    ENDIF = 9

    WHILE = 16
    ENDWHILE = 17

    DEF = 32
    ENDDEF = 33

    CLASS = 64
    ENDCLASS = 65


class Token:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value


NONE = Token(TokenKind.NONE)


class Lex:
    def __init__(self, stream):
        self._s = stream
        self._last = None
        self._m = []

    def mark(self):
        self._m.append(self._s.tell())

    def remark(self):
        if not self._m:
            self.mark()
        else:
            self._m[-1] = self._s.tell()

    def unmark(self):
        if self._m:
            self._m.pop()

    def jump(self):
        if self._m:
            self._s.seek(self._m.pop())

    def read(self, n=1):
        ch = self._s.read(n)
        if not ch:
            raise StopIteration()
        return ch

    def peek(self, n=1):
        self.mark()
        self._last = self._s.read(n)
        self.jump()
        return self._last

    def consume(self):
        if not self._last:
            return
        self._s.seek(self._s.tell() + len(self._last))

    def peek_and_consume(self, expected_str):
        print("Peek and consume expected:", expected_str)
        if self.peek(len(expected_str)) == expected_str:
            self.consume()
            return True
        return False

    def next(self):
        tok = NONE

        self.mark()

        if self.peek_and_consume(";"):
            tok = Token(TokenKind.SEMI, ";")
        elif self.peek_and_consume(":"):
            tok = Token(TokenKind.COLON, ":")

        if tok != NONE:
            # Consume consecutive whitespace after the (semi)colon.
            while self.peek_and_consume(" "):
                self.remark()

            self.unmark()
            return tok

        # Try handling some keywords...
        if self.peek_and_consume("if"):
            tok = Token(TokenKind.IF, "if")
        elif self.peek_and_consume("endif"):
            tok = Token(TokenKind.ENDIF, "endif")
        elif self.peek_and_consume("while"):
            tok = Token(TokenKind.WHILE, "while")
        elif self.peek_and_consume("endwhile"):
            tok = Token(TokenKind.ENDWHILE, "endwhile")
        elif self.peek_and_consume("def"):
            tok = Token(TokenKind.DEF, "def")
        elif self.peek_and_consume("enddef"):
            tok = Token(TokenKind.ENDDEF, "enddef")
        elif self.peek_and_consume("class"):
            tok = Token(TokenKind.CLASS, "class")
        elif self.peek_and_consume("endclass"):
            tok = Token(TokenKind.CLASS, "endclass")

        # Now that keywords have been consumed if any found, see if the next
        # char is a whitespace separator.
        ch = self.peek(1)
        print("Ater kw handling read", ch)
        if (not ch or ch in [' ', '\n', '\t', '\r', '(', '[', '{', '}', ']',
                             ')', ':', ';', '/', '\\', '+', '-', '*', '#',
                             '?']) \
                and tok != NONE:
            print("Separated kw.")
            # Yay, the token is separated and not continued with a letter or
            # number.
            self.unmark()
            return tok
        else:
            print("continuing text, not kw...")
            # Nay, the token continues with a different letter, so it's not a
            # keyword by itself.
            self.jump()  # Jump back to beginning of token.
            self.mark()  # And reinstate the marker.

        chars = []
        while True:
            try:
                ch = self.read(1)
                print("Continue read", ch)

                if ch == ";" or ch == ":":
                    # (Semi)colon encountered, break off the current token.
                    self.jump()  # ... *before* the semi.
                    break
                if ch == " ":
                    print("SPACE.")
                    # Whitespace encountered, break off the token, but consume
                    # the whitespace.
                    chars.append(ch)
                    break

                chars.append(ch)
                self.remark()  # Set last read char position.
            except StopIteration:
                print("StopIteration.", chars)
                if not chars:
                    # If nothing is read and we are at the end, produce EOF.
                    self.unmark()
                    return Token(TokenKind.EOF)
                # Otherwise, go and return what was collected.
                break

        self.unmark()  # Drop the seekback marker of this call.
        print("End.", chars)
        string = "".join(chars)
        if string.strip() == "":
            return NONE

        return Token(TokenKind.UNINTERESTING, string)
