"""
Docstring for scripts.poetry_runner
"""

#!/usr/bin/env python3
import subprocess
from pathlib import Path


def run_all_tests():
    script = Path(__file__).parent / "run-tests.sh"
    subprocess.run([script])
