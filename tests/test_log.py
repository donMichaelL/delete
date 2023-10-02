import logging


def test_default_logging_configuration(setup_imports):
    """Check the default logging config."""
    from theTrial.utils.log import configure_logging

    configure_logging()

    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]
    formatter = handler.formatter

    assert handler.level == logging.INFO
    assert isinstance(handler, logging.StreamHandler)
    assert formatter.datefmt == "%H:%M:%S"
    assert formatter._fmt == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
