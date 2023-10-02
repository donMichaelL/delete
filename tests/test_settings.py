import pytest


@pytest.fixture(scope="module")
def settings_imports(setup_imports):
    """Import required utility functions after patching imports."""
    from theTrial.settings import load_settings

    return load_settings


def test_default_settings_module_name(settings_imports):
    """Check default module is settings."""
    settings = settings_imports
    assert settings.settings_module == "settings"


def test_settings_load_uppercase_variables(settings_imports):
    """Check uppercase variables are loaded."""
    settings = settings_imports
    assert hasattr(settings, "UPPERCASE_VAR")
    assert settings.UPPERCASE_VAR == "UPPERCASE_VALUE"


def test_settings_variables_must_be_uppercase(settings_imports):
    """Check lowercase variables are not loaded."""
    settings = settings_imports
    assert not hasattr(settings, "lowercase_var")


def test_settings_can_change_attribute(settings_imports):
    """Check settings can change."""
    settings = settings_imports
    settings.UPPERCASE_VAR = "new_value"
    assert settings.UPPERCASE_VAR == "new_value"
