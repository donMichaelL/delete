# noqa: INP001
import re
from pathlib import Path

from setuptools import setup

# Path to __init__.py
init_path = Path("src/theTrial/__init__.py")

# Extract version using regex
content = init_path.read_text()
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

setup(
    version=version,
)
