import os

from setuptools import find_packages
from setuptools import setup

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_readme():
  try:
    readme = open(
        os.path.join(_CURRENT_DIR, "README.md"), encoding="utf-8").read()
  except OSError:
    readme = ""
  return readme


def _get_version(): return "5.1.0"

_VERSION = _get_version()
_README = _get_readme()

setup(
    name="plotille",
    version=_VERSION,
    description="package for terminal plotting",
    long_description="\n".join([_README]),
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
