import os
import sys
from glob import glob

import pytest


@pytest.fixture
def change_to_examples_dir(request):
    os.chdir(request.fspath.dirname + "/../examples")
    yield
    os.chdir(str(request.config.invocation_dir))


def test_examples(change_to_examples_dir):
    sys.path.insert(0, ".")
    for fname in glob("*_example.py"):
        print(fname)
        name = fname.split(".")[0]
        example_module = __import__(name)
        example_module.main()
