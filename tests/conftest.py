import pytest
import json


@pytest.fixture
def factory():
    def _factory(path):
        with open(path, 'r') as fd:
            return json.loads(fd.read())
    return _factory
