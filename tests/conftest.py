import sys
import os
import pytest

#Execure the following code only once per session
@pytest.fixture(scope="session", autouse=True)
def setup():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))