# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: json.py
# Title: JSON filter and transformer
# Description: Loads a JSON from the standard input, offers it for
# Description: transformation, and after, writes it to the standard output.
#
# Var: DATA - the input parsed to JSON, in whatever format the input represents
#
# Fun: PRETTY - Enable prettified JSON output.
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
import json
import sys


ARGS = sys.argv
__PRETTY_JSON__ = False


def PRETTY():
    global __PRETTY_JSON__
    __PRETTY_JSON__ = True


DATA = json.load(sys.stdin)


# --- USER CODE GOES HERE ---


if not __PRETTY_JSON__:
    print(json.dumps(DATA))
else:
    print(json.dumps(DATA, sort_keys=True, indent=4))

# ---  END  TEMPLATE ---
