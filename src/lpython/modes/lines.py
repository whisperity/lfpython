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
# Fun: OUT(...) - write to the standard output
# Fun: ERR(...) - write to the standard error
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
import fileinput
import sys


def OUT(*args):
    print(*args, end='')


def ERR(*args):
    print(*args, end='', file=sys.stderr)


print("RUNNING", __file__)

for LINE in fileinput.input("-"):
    # --- USER CODE GOES HERE ---
    pass

# ---  END  TEMPLATE ---
