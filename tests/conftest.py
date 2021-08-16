import pytest


@pytest.fixture(autouse=True, scope="function")
def isolate(fn_isolation):
    pass
