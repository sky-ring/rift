import pytest

from rift.runtime.config import Config
from rift.ast.sentry.watchers.import_restrictor import allowed_imports


@pytest.fixture(autouse=True)
def setup_env():
    Config.TEST = True
    allowed_imports.append("test")
    yield
    Config.TEST = False
    allowed_imports.append("test")
