# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: csv.py
# Title: CSV filter and transformer
# Description: Loads a CSV from the standard input, and executes the user code
# Description: in a loop for each row, allowing transformation. After that,
# Description: writes the CSV file to the standard output.
#
# Var: ROW - one row from the input to be handled.
#
# Fun: HEADER() - True if the first row is in ROW, False otherwise.
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
import csv
import sys


ARGS = sys.argv
__READER__ = csv.reader(sys.stdin)
__OUTPUT__ = []
__HEADER__ = True

def HEADER():
    return __HEADER__


for ROW in __READER__:
    # --- USER CODE GOES HERE ---

    __OUTPUT__.append(ROW)
    if __HEADER__:
        __HEADER__ = False


__WRITER__ = csv.writer(sys.stdout)
__WRITER__.writerows(__OUTPUT__)

# ---  END  TEMPLATE ---
