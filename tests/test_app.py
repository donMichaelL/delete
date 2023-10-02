from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.fixture(scope="module")
def trial(setup_imports):
    """Patch KafkaProducer/KafkaConsumer and yield an instance of TheTrial."""
    with patch.multiple(
        "theTrial.app", KafkaProducer=MagicMock(), KafkaConsumer=MagicMock()
    ):
        from theTrial import TheTrial

        yield TheTrial()


def test_can_add_function(trial):
    """New handler function for a topic can be added."""
    func = lambda x: x  # noqa: E731
    trial.add_function("topic1", func)
    assert func in trial.consumer_map["topic1"]


def test_intopic_decorator(trial):
    """Intopic decorator adds a function to the consumer_map for a topic."""

    @trial.intopic("topic2")
    def sample_func(x):
        return x * 2

    assert len(trial.consumer_map["topic2"]) == 1
    assert trial.consumer_map["topic2"][0](2) == 4


def test_outopic_decorator(trial, mocker):
    """Outopic decorator sends the expected message using the producer."""
    mock_result = mocker.Mock()
    mock_result.json.return_value = {"value": 10}

    @trial.outopic("topic3")
    def sample_func():
        return mock_result

    sample_func()
    trial.producer.send_message.assert_called_with(topic="topic3", msg={"value": 10})


def test_stop_method(trial, mocker):
    """The stop method sets the terminate_event."""
    mock_set = mocker.Mock()
    trial.terminate_event.set = mock_set
    trial.stop()
    mock_set.assert_called_once()


def test_run_method_starts_thread(trial, mocker):
    """Test that the run method starts a new thread for the consumer."""
    mock_thread = mocker.Mock()
    mocker.patch("theTrial.app.Thread", return_value=mock_thread)
    trial.run()
    mock_thread.start.assert_called_once()
