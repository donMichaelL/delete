import logging.config

from ..settings import load_settings as setting

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
    },
}


def configure_logging() -> None:
    """
    Configure the logging settings for the application.

    This function checks if the `CONFIG_LOGGING` attribute is set in
    the `setting` module. If it's set, it will use that configuration.
    Otherwise, it will default to using the `DEFAULT_LOGGING` configuration.

    """
    config = getattr(setting, "CONFIG_LOGGING", DEFAULT_LOGGING)
    logging.config.dictConfig(config)
