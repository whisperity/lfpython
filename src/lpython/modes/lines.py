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

print("Template code BEFORE")

if False:
    # --- USER CODE GOES HERE ---
    pass

print("Template code AFTER")

if True:
    print("End.")

# ---  END  TEMPLATE ---
