import io
import shutil
import sys

from .args import args
from .builder import load
from .parser import Parser
from .tokeniser import Lex


def transpile(codeStream, outputStream):
    """Rewrites the input stream of program code according to LPython rules."""
    lexer = Lex(codeStream)
    parser = Parser(lexer)

    while not parser.eof:
        stmt = parser.parse()
        outputStream.write(stmt)

    return outputStream


def build(mode, codeStream, outputStream):
    """Inject the given program code into the template specified by 'mode'
    into the outputStream."""
    codeStream.seek(0)

    context = load(mode)
    result = context(codeStream)

    result.seek(0)
    outputStream.seek(0)
    shutil.copyfileobj(result, outputStream)
    return outputStream


def main(argv):
    """The real entry point handler for the program."""
    argd = args.parse_args(argv)

    if not argd.CODE and argd.mode:
        # No code specified, but a mode was specified.
        print("No code specified. Showing help for '%s'..." % argd.mode,
              file=sys.stderr)
        template = load(argd.mode)
        print("Name:", template.name)
        print("Title:", template.title)
        print("Description:", template.description)
        print()
        print("Available variables:")
        for var in template.vars:
            print("  *", var)
        print()
        print("Available functions:")
        for fun in template.funs:
            print("  *", fun)
        return 1

    code_in = io.StringIO(" ".join(argd.CODE))
    code_out = io.StringIO()
    transpile(code_in, code_out)

    if argd.dry_run:
        # Dry run - emit only the rewritten code.
        print(code_out.getvalue())
        return 0

    result = io.StringIO()
    build(argd.mode, code_out, result)

    if argd.build_only:
        print(result.getvalue())
        return 0

    print("TODO: Execution...")
