import importlib

from environs import Env

env = Env()

__all__ = [
    "load_settings",
]


class Settings:
    def __init__(self):
        """
        Initialize the Settings class. The settings are loaded from the module
        specified in the Config's SETTINGS_MODULE attribute.
        """
        self.settings_module = env.str("SETTINGS_MODULE", "settings")
        self._load_settings()

    def _load_settings(self) -> None:
        """
        Load settings from the module specified by the instance variable.
        For each setting in the module, if the setting name is uppercase,
        add it to the config instance as a dynamic field.
        """
        mod = importlib.import_module(self.settings_module)
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))


load_settings = Settings()
