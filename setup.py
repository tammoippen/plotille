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
    name = "plotille"
    , version = _VERSION
    , description = "Plot in the terminal using braille dots."
    , authors = ["Tammo Ippen <tammo.ippen@posteo.de>"]
    , license = "MIT"
    , readme = "README.md"

    , classifiers = [
# Trove classifiers
# Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Terminals'
        ]

    , long_description="\n".join([_README])
    , long_description_content_type="text/markdown"

    , packages=find_packages()
)
