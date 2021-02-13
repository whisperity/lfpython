lpython: Linear Python scripts
==============================

**`lpython`** allows executing "Python"-ish scripts in the command line as parts of a pipeline.

_Why?_ Normally, the Python binary allows executing Python script specified in the command-line, but you have to write a proper Python script:

~~~~
python3 -c 'import json
print(json.dumps({0: 1}))
'
~~~~

This may make shell history unreadable, hard to edit, etc.

In addition, accessing information in a pipe, common with most command-line tools, is convoluted.
While you can easily say `some-command-generating-data | grep Foo | awk '{ print $2; }'`, doing a similar thing for data processing in Python is really hard, requiring you to open an editor, save a script file.

**`lpython`** takes this need off for **quick and dirty** command-line data processing.

Overview
--------

> **TODO.**

Syntax
------

The code given to `lpython` is generally the same as normal Python code, except for a few key differences:

 * **Lines are terminated by `;` (semicolon)**, instead of a newline. Newlines still work, but the entire idea is to not deal with newlines.
 * Due to not dealing with newlines and whitespace, the indentation-based "scoping" is also side-stepped:
    * Everything that would begin a scope and require indented code is instead closed with an `endX` keyword.
    * For example: `if X: print(X); endif;`, `while True: endwhile;`, `def identity(a): return a; enddef`.

Everything else in-between is expected to behave as it would in Python.
