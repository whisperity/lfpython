import io
import shutil
import sys

from .args import args
from .builder import load
from .parser import Parser
from .spawn import temporary, spawn
from .tokeniser import Lex


def transpile(code_stream, output_stream, debug_lex=False, debug_parse=False):
    """Rewrites the input stream of program code according to LPython rules."""
    lexer = Lex(code_stream, debug_lex)
    parser = Parser(lexer, debug_parse)

    while not parser.eof:
        stmt = parser.parse()
        output_stream.write(stmt)

    return output_stream


def build(mode, code_stream, output_stream):
    """Inject the given program code into the template specified by 'mode'
    into the outputStream."""
    code_stream.seek(0)

    context = load(mode)
    result = context(code_stream)

    result.seek(0)
    output_stream.seek(0)
    shutil.copyfileobj(result, output_stream)
    return output_stream


def main(argv=None):
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
    transpile(code_in, code_out, argd.verbose_lex, argd.verbose_parse)

    if argd.dry_run:
        # Dry run - emit only the rewritten code.
        print(code_out.getvalue())
        return 0

    result = io.StringIO()
    build(argd.mode, code_out, result)

    if argd.build_only:
        print(result.getvalue())
        return 0

    if argd.verbose_lex or argd.verbose_parse:
        return 0

    with temporary(result) as script:
        return_code = spawn(script, argd.argfwd)

    return return_code
