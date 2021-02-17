# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: lines.py
# Title: line-by-line text operation
# Description: Executes the script in a loop that iterates over every line in
# Description: the standard input. The user's code is automatically placed
# Description: inside an appropriate loop.
#
# Var: LINE - one line from the input as handled in the loop.
#
# Fun: OUT(...) - write to the standard output, explicitly (no newline at end)
# Fun: ERR(...) - write to the standard error, explicitly (no newline at end)
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
import fileinput
import sys


ARGS = sys.argv


def OUT(*args):
    print(*args, end='')


def ERR(*args):
    print(*args, end='', file=sys.stderr)


for LINE in fileinput.input("-"):
    if LINE[-1] == "\n":
        LINE = LINE[:-1]
    # --- USER CODE GOES HERE ---
    pass

# ---  END  TEMPLATE ---
