# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: bare.py
# Title: bare stream handling
# Description: The script given by the user is executed verbatim.
# Description: This mode performs no additional operation and offers no
# Description: helping logic.
#
# Var: STDIN - the Python sys.stdin stream
# Var: STDOUT - the Python sys.stdout stream
# Var: STDERR - the Python sys.stderr stream
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
import sys


ARGS = sys.argv
STDIN = sys.stdin
STDOUT = sys.stdout
STDERR = sys.stderr


# --- USER CODE GOES HERE ---


# ---  END  TEMPLATE ---
