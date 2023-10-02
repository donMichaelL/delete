__version__ = "0.0.2"


# If the script is being run as a standalone script (from the CLI)
# pass exception to avoid crashing due to missing modules when running in CLI

try:
    from .app import TheTrial  # noqa: F401
    from .utils.log import configure_logging

    configure_logging()
except ImportError:
    pass
