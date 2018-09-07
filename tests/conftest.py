import json
import os

import pytest


@pytest.fixture
def factory():
    def _factory(filename):
        path = os.path.dirname(os.path.abspath(__file__))
        path_factory = os.path.join(path, 'factory', filename)
        with open(path_factory, 'r') as fd:
            return json.loads(fd.read())
    return _factory
