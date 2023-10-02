import logging
from unittest.mock import MagicMock

import pytest
from confluent_kafka import KafkaError


class MockMessage:
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value


class CustomMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = kwargs["error"]

    def produce(self, topic, value, callback):
        if self.error:
            callback(KafkaError, None)
        else:
            callback(None, MockMessage("Test Message"))

    def flush(self):
        ...


@pytest.fixture(
    params=[(None, "Message produced"), (True, "Failed to deliver message")]
)
def kafka_producer_setup(mocker, setup_imports, request):
    """Parametrized fixture to setup KafkaProducer with different error conditions
    and expected log messages.
    """
    from theTrial.kafka.producer import KafkaProducer

    error_flag, log_message = request.param
    mock_producer = CustomMock(error=error_flag)
    mocker.patch("theTrial.kafka.producer.Producer", return_value=mock_producer)
    producer_instance = KafkaProducer({})
    return producer_instance, log_message


def test_kafka_producer_send(kafka_producer_setup, caplog):
    """Test the behavior of producer send message under various conditions."""
    caplog.set_level(logging.INFO)
    kafka_producer, expected_log_message = kafka_producer_setup
    kafka_producer.send_message("test_topic", "Test Message")
    assert expected_log_message in caplog.text
