import subprocess
import sys

with open("pytest_output.txt", "w") as f:
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=True, text=True)
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\nSTDERR:\n")
    f.write(result.stderr)
    f.write(f"\nRETURN CODE: {result.returncode}\n")
