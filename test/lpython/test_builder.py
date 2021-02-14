import io
import pytest

from lpython.builder import ExecutionContext as C

user_code = """user1()
user2()
if user3():
    print("Y")"""

dummy_header = """# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: dummy.py
# Title: Dummy
# Description: Dummy A
# Description: B
# Var: VAR1
# Var: VAR2
# Fun: FUN1
# Fun: FUN2
# ---  END  METADATA ---
#
# --- BEGIN TEMPLATE ---
"""

dummy_empty = dummy_header + """
# ---  END  TEMPLATE ---
"""

dummy_trivial = dummy_header + """
# --- USER CODE GOES HERE ---
# ---  END  TEMPLATE ---
"""

dummy_simple = dummy_header + """
print("X")
# --- USER CODE GOES HERE ---
# ---  END  TEMPLATE ---
"""

dummy_multiple = dummy_header + """
# --- USER CODE GOES HERE ---
if not lpython:
    # --- USER CODE GOES HERE ---
# ---  END  TEMPLATE ---
"""

dummy_complex = dummy_header + """
if sys:
    # --- USER CODE GOES HERE ---
# ---  END  TEMPLATE ---
"""

dummy_pass = dummy_header + """
if sys:
    # --- USER CODE GOES HERE ---
    pass
pass
if other:
    pass
# ---  END  TEMPLATE ---
"""


def test_invalid_format():
    with pytest.raises(ValueError) as ve:
        C(dummy_header)
    assert("'# ---  END  TEMPLATE ---' is not in" in str(ve.value))


def test_empty():
    with pytest.raises(ValueError) as ve:
        C(dummy_empty)
    assert("No insertion line" in str(ve.value))


def test_trivial():
    expected = """
user1()
user2()
if user3():
    print("Y")
"""

    c = C(dummy_trivial)
    x = c(io.StringIO(user_code)).getvalue()
    assert(x == expected)


def test_simple():
    expected = """
print("X")
user1()
user2()
if user3():
    print("Y")
"""

    c = C(dummy_simple)
    x = c(io.StringIO(user_code)).getvalue()
    assert(x == expected)


def test_multiple():
    with pytest.raises(ValueError) as ve:
        C(dummy_multiple)
    assert("Multiple insertion" in str(ve.value))


def test_complex():
    expected = """
if sys:
    user1()
    user2()
    if user3():
        print("Y")
"""

    c = C(dummy_complex)
    x = c(io.StringIO(user_code)).getvalue()
    assert(x == expected)


def test_pass():
    expected = """
if sys:
    user1()
    user2()
    if user3():
        print("Y")
pass
if other:
    pass
"""

    c = C(dummy_pass)
    x = c(io.StringIO(user_code)).getvalue()
    assert(x == expected)
