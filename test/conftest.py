import pytest
from rift.runtime.config import Config


@pytest.fixture(autouse=True)
def setup_env():
    Config.TEST = True
    yield
    Config.TEST = False
