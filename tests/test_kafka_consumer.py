import sys
from threading import Event

import pytest


class MockMessage:
    def __init__(self, topic, value):
        self._topic = topic
        self._value = value

    def topic(self):
        return self._topic

    def value(self):
        return self._value

    def error(self):
        return None


class MockModel:
    def parse_raw(msg):
        return MockModel()


def handler_no_args():
    pass


def handler_one_arg_msg(msg: MockModel):
    pass


def handler_two_arg_msg(msg: MockModel, topic: str):
    pass


@pytest.fixture(scope="module")
def mock_message():
    """Return a mock message"""
    topic, encoded_msg = "test_topic", b"test_message"
    return MockMessage(topic, encoded_msg)


@pytest.fixture
def kafka_consumer_setup(mocker, setup_imports):
    """Mock and setup a KafkaConsumer with predefined poll behavior
    and termination event."""
    from theTrial.kafka.consumer import KafkaConsumer

    def poll_side_effect(*args, **kwargs):
        topic, encoded_msg = "test_topic", b"test_message"
        terminate_event.set()
        return MockMessage(topic, encoded_msg)

    consumer_mock = mocker.MagicMock()
    terminate_event = Event()
    kafka_consumer = KafkaConsumer({"group.id": 12}, terminate_event=terminate_event)
    kafka_consumer.consumer = consumer_mock
    consumer_mock.subscribe.return_value = None
    consumer_mock.poll.side_effect = poll_side_effect
    return kafka_consumer


def test_call_handlers_no_key_error_if_topic_not_in_handlers(
    mocker, setup_imports, mock_message
):
    """If topic not in topic_handler's key thenm no raised exception."""
    from theTrial.kafka.consumer import call_handlers

    spy_no_args = mocker.spy(sys.modules[__name__], "handler_no_args")
    topic_handlers = {"topic": [handler_no_args]}
    call_handlers(topic_handlers, mock_message)
    assert spy_no_args.call_count == 0


def test_no_args_handler(mocker, setup_imports, mock_message):
    """When handler has no args and just called."""
    from theTrial.kafka.consumer import call_handlers

    spy_no_args = mocker.spy(sys.modules[__name__], "handler_no_args")
    topic_handlers = {mock_message.topic(): [handler_no_args]}
    call_handlers(topic_handlers, mock_message)
    spy_no_args.assert_called_once()


def test_one_arg_handler(mocker, setup_imports, mock_message):
    """When handler has 1 arg which is only the message."""
    from theTrial.kafka.consumer import call_handlers

    spy = mocker.spy(sys.modules[__name__], "handler_one_arg_msg")
    topic_handlers = {mock_message.topic(): [handler_one_arg_msg]}
    call_handlers(topic_handlers, mock_message)
    spy.assert_called_once()
    args, _ = spy.call_args
    assert len(args) == 1
    assert isinstance(args[0], MockModel)


def test_two_arg_handler(mocker, setup_imports, mock_message):
    """When handler has 2 args which are the message and the topic."""
    from theTrial.kafka.consumer import call_handlers

    spy = mocker.spy(sys.modules[__name__], "handler_two_arg_msg")
    topic_handlers = {mock_message.topic(): [handler_two_arg_msg]}
    call_handlers(topic_handlers, mock_message)
    spy.assert_called_once()
    args, _ = spy.call_args
    assert len(args) == 2
    assert isinstance(args[0], MockModel)
    assert args[1] == "test_topic"


def test_consume_message(mocker, kafka_consumer_setup):
    """Consume method correctly calls the handler for received Kafka messages."""
    from theTrial.kafka import consumer

    def handler_no_args():
        pass

    topic_handlers = {"test_topic": [handler_no_args]}
    spy = mocker.spy(consumer, "call_handlers")
    kafka_consumer_setup.consume(topic_handlers)
    spy.assert_called_once()
    args, _ = spy.call_args
    assert len(args) == 2
    assert args[0] == topic_handlers
    assert isinstance(args[1], MockMessage)
