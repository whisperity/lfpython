import argparse

from .builder import load_all

args = argparse.ArgumentParser(
        prog="lpython",
        description="Rewrite Python scripts written in a linear code fashion "
                    "to real Python scripts, and execute them for quick & "
                    "dirty shell pipeline operations.",
        epilog="Linear Python scripts differ from real Python in a few "
               "crucial ways. First, there is no need to handle indentation, "
               "because it is meant to be written in one line like a shell "
               "command. Second, there is no need for newlines, as the "
               "semicolon (';') line separator, common in many other "
               "programming languages, have been reintroduced. To emphasise "
               "blocks, instead of indentation, explicit closing keywords are "
               "used: \"with X: print(); endwith;\"."
        )

args.add_argument("-n",
                  dest="dry_run",
                  action="store_true",
                  help="Do not execute, just rewrite the input code, without "
                       "the execution context, as Python script and emit the "
                       "result to the standard output.")

args.add_argument("-b",
                  dest="build_only",
                  action="store_true",
                  help="Do not execute, but rewrite the input code and build "
                       "the full execution context, and emit the result to "
                       "the standard output.")

args.add_argument("-vl",
                  dest="verbose_lex",
                  action="store_true",
                  help="Enable verbose debugging messages of the lexer's "
                       "internal workings. Implies disabling execution.")

args.add_argument("-vp",
                  dest="verbose_parse",
                  action="store_true",
                  help="Enable verbose debugging messages of the parser's "
                       "internal workings. Implies disabling execution.")

args.add_argument("-t",
                  dest="mode",
                  choices=list(map(lambda c: c.name, load_all())),
                  default="lines",
                  help="The operational framework to embed the script into "
                       "during execution. Different choices here affect what "
                       "variables are available during execution and how the "
                       "code is structured. When called with a '-t' argument "
                       "but without code to execute, a help text about the "
                       "specified mode is shown."
                  )

args.add_argument("-X",
                  dest="argfwd",
                  metavar="arg",
                  action='append',
                  help="Forward the arguments in the order they are specified "
                       "to the executed script. To forward more arguments, "
                       "specify the option multiple times: "
                       "\"-X arg1 -X arg2\".")

args.add_argument("CODE",
                  nargs="*",
                  help="The LPython code to transpile and execute.")
