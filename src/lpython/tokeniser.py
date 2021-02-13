from enum import Enum


class TokenKind(Enum):
    NONE = -1
    UNINTERESTING = 0
    EOF = 1
    SEMI = 2
    COLON = 3
    OPEN = 4
    CLOSE = 5

    IF = 8
    ENDIF = 9

    WHILE = 16
    ENDWHILE = 17
    FOR = 18
    ENDFOR = 19

    WITH = 32
    ENDWITH = 33

    DEF = 64
    ENDDEF = 65

    CLASS = 128
    ENDCLASS = 129


class Token:
    def __init__(self, kind, pos, value=""):
        self.kind = kind
        self.position = pos
        self.value = value

    def __repr__(self):
        return "T<%d(%s), %d, \"%s\">" % (self.kind.value, self.kind.name,
                                          self.position, self.value)


NONE = Token(TokenKind.NONE, -1)

EOF_MAGIC = " <<<EOF>>>"

WHITESPACE = [' ', '\n', '\t', '\r']

TOKEN_BREAKERS = ['(', '[', '{', '}', ']', ')', ':', ';', '/', '\\', '+', '-',
                  '*', '#', '?']


class Lex:
    def __init__(self, stream):
        self._s = stream
        self._last = None
        self._m = []

    def mark(self):
        """Saves the current position into the jumpback stack."""
        self._m.append(self._s.tell())
        return self._s.tell()

    def remark(self):
        """Changes the last marked jumpback to the current position."""
        if not self._m:
            self.mark()
        else:
            self._m[-1] = self._s.tell()

    def unmark(self):
        """Removes the last jumpback position."""
        if self._m:
            self._m.pop()

    def jump(self):
        """Jumps back to the last jumpback position, and consumes it."""
        if self._m:
            self._s.seek(self._m.pop())

    def read(self, n=1):
        """Read n characters from the input, advancing the stream."""
        ch = self._s.read(n)
        if not ch:
            raise StopIteration()
        return ch

    def peek(self, n=1):
        """Read n characters from the input, but do not advance the stream."""
        self.mark()
        self._last = self._s.read(n)
        self.jump()
        return self._last

    def seek_and_peek(self, p=0, n=1):
        """Jumps to the position p and reads n characters, but then returns to
        the previous position."""
        self.mark()
        self._s.seek(p)
        ret = self._s.read(n)
        self.jump()
        return ret

    def consume(self):
        """Advances the stream's position with the last peek result's token."""
        if not self._last:
            return
        self._s.seek(self._s.tell() + len(self._last))

    def peek_and_consume(self, expected_str):
        """Peek the stream for the length of the expected string, and if found,
        consume the input.

        Returns True if the expected string was found.
        """
        if self.peek(len(expected_str)) == expected_str:
            self.consume()
            return True
        return False

    def next(self):
        """Lexes the next token."""
        tok = NONE

        pos = self.mark()

        symbol_kind = TokenKind.NONE
        if self.peek_and_consume(";"):
            symbol_kind = TokenKind.SEMI
        elif self.peek_and_consume(":"):
            symbol_kind = TokenKind.COLON
        elif self.peek_and_consume("("):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume("["):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume("{"):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume(")"):
            symbol_kind = TokenKind.CLOSE
        elif self.peek_and_consume("]"):
            symbol_kind = TokenKind.CLOSE
        elif self.peek_and_consume("}"):
            symbol_kind = TokenKind.CLOSE

        if symbol_kind != TokenKind.NONE:
            # Consume consecutive whitespace after the symbols.
            token_text = self._last
            while self.peek_and_consume(" "):
                self.remark()
                token_text += self._last

            self.unmark()
            return Token(symbol_kind, pos, token_text)

        # Try handling some keywords...
        kw_kind = TokenKind.NONE
        if self.peek_and_consume("if"):
            kw_kind = TokenKind.IF
        elif self.peek_and_consume("endif"):
            kw_kind = TokenKind.ENDIF
        elif self.peek_and_consume("while"):
            kw_kind = TokenKind.WHILE
        elif self.peek_and_consume("endwhile"):
            kw_kind = TokenKind.ENDWHILE
        elif self.peek_and_consume("for"):
            kw_kind = TokenKind.FOR
        elif self.peek_and_consume("endfor"):
            kw_kind = TokenKind.ENDFOR
        elif self.peek_and_consume("with"):
            kw_kind = TokenKind.WITH
        elif self.peek_and_consume("endwith"):
            kw_kind = TokenKind.ENDWITH
        elif self.peek_and_consume("def"):
            kw_kind = TokenKind.DEF
        elif self.peek_and_consume("enddef"):
            kw_kind = TokenKind.ENDDEF
        elif self.peek_and_consume("class"):
            kw_kind = TokenKind.CLASS
        elif self.peek_and_consume("endclass"):
            kw_kind = TokenKind.ENDCLASS

        if kw_kind != TokenKind.NONE:
            tok = Token(kw_kind, pos, self._last)

        # Now that keywords have been consumed if any found, see if the next
        # char is a whitespace separator.
        ch = self.peek(1)
        if (not ch or ch in WHITESPACE or ch in TOKEN_BREAKERS) \
                and tok != NONE:
            # Yay, the token is separated and not continued with a letter or
            # number.
            self.unmark()
            return tok
        else:
            # Nay, the token continues with a different letter, so it's not a
            # keyword by itself.
            self.jump()  # Jump back to beginning of token.
            self.mark()  # And reinstate the marker.

        chars = []
        while True:
            try:
                ch = self.read(1)
                if ch in TOKEN_BREAKERS:
                    # Token breaker encountered.
                    self.jump()  # ... *before* the token.
                    break
                if ch in WHITESPACE:
                    # Whitespace encountered, break off the token, but consume
                    # the whitespace.
                    chars.append(ch)
                    break

                chars.append(ch)
                self.remark()  # Set last read char position.
            except StopIteration:
                if not chars:
                    # If nothing is read and we are at the end, produce EOF.
                    self.unmark()
                    self._s.write(EOF_MAGIC)
                    return Token(TokenKind.EOF, pos, EOF_MAGIC)
                # Otherwise, go and return what was collected.
                break

        self.unmark()  # Drop the seekback marker of this call.
        string = "".join(chars)
        if string.strip() == "":
            return NONE
        return Token(TokenKind.UNINTERESTING, pos, string)
