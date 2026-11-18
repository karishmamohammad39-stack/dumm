import pytest
import sys

if __name__ == "__main__":
    sys.exit(pytest.main(["tests/core/test_io.py", "--cov=src.core.io", "--cov-report=term-missing"]))
