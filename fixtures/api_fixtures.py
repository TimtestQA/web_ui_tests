import pytest
from helpers.api_helper import APIHelper

@pytest.fixture(scope="module")
def api_helper():
    yield APIHelper()