from contextlib import contextmanager
import os
import shutil
from subprocess import run
import sys
import tempfile


@contextmanager
def temporary(code_buffer):
    with tempfile.TemporaryDirectory(prefix="lpython-") as tempdname:
        filename = os.path.join(tempdname, "code.py")
        with open(filename, "w") as script:
            code_buffer.seek(0)
            shutil.copyfileobj(code_buffer, script)

        yield filename


def spawn(pyscript, argv):
    """Spawns a process and gives it our stdin and stdout."""
    interp = sys.executable if sys.executable else "python3"
    argv = argv if argv else []
    result = run([interp, pyscript] + argv, text=True)
    return result.returncode
