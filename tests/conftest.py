import importlib
import unittest.mock

import pytest


class MockSettingsModule:
    UPPERCASE_VAR = "UPPERCASE_VALUE"
    CONFIG_PRODUCER = "configuration"
    lowercase_var = "lowercase_value"


@pytest.fixture(scope="module")
def setup_imports():
    """Patch 'import_module' to always return the 'MockSettingsModule'."""

    def import_side_effect(name, *args, **kwargs):
        """If the module being imported is "settings", return the mocked module.
        Otherwise, defer to the original import_module function.
        """
        if name == "settings":
            return MockSettingsModule
        else:
            return original_import_module(name, *args, **kwargs)

    original_import_module = importlib.import_module

    with unittest.mock.patch.object(
        importlib, "import_module", side_effect=import_side_effect
    ):
        yield
