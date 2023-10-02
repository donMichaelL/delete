from threading import Event
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka.cimpl import Message

from . import logger
from ..settings import load_settings as settings
from ..utils.inspect_function import get_signature_details


KafkaTopic = NewType("KafkaTopic", str)
TopicCallableMap = Dict[KafkaTopic, List[Callable[..., Any]]]


def call_handlers(topic_handlers: TopicCallableMap, msg: Message) -> None:
    """
    Process a Kafka message by calling the appropriate handler
    functions based on the topic.

    This function decodes the received message and determines the
    appropriate handler function(s) to call based on the message's topic.
    The handler is then called with arguments based on itssignature.
    Handlers can have 0, 1, or 2 parameters:

    - 0 parameters: The handler is called with no arguments.
    - 1 parameter: The handler is called with the decoded message.
    - 2 parameters: The handler is called with the decoded message and the topic.

    :param topic_handlers: A mapping of topics to their associated handler functions.
    :param msg: The received Kafka message.
    """
    topic, decoded_msg = msg.topic(), msg.value().decode("utf-8")
    for func in topic_handlers.get(topic, []):
        total_params, first_arg_type = get_signature_details(func)
        if total_params == 0:
            func()
        elif total_params == 1:
            func(first_arg_type.parse_raw(decoded_msg))
        elif total_params == 2:
            func(first_arg_type.parse_raw(decoded_msg), topic)


class KafkaConsumer:
    """
    A simple Kafka consumer class for consuming messages from Kafka topics.

    This class wraps the basic functionality of the Confluent Kafka Consumer,
    providing a straightforward interface for consuming messages.
    """

    def __init__(
        self, config: Optional[dict] = None, terminate_event: Optional[Event] = None
    ):
        """
        Initialize the KafkaConsumer instance.

        If a configuration dictionary is provided, it will be used to configure
        the Kafka consumer.
        If not, the default configuration from settings.CONFIG_CONSUMER will be used.

        :param config: Configuration dictionary for the Kafka consumer. If None,
                       defaults to settings.CONFIG_CONSUMER.
        :param terminate_event: An optional threading.Event that can be used to signal
                       the consumer to terminate.
        """
        self.consumer = Consumer(config or settings.CONFIG_CONSUMER)  # type: ignore
        self.terminate_event = terminate_event

    def consume(self, topic_handlers: TopicCallableMap) -> None:
        """
        Continuously consume messages from Kafka topics and process them by
        calling using call_handlers. The loop continues until the `terminate_event`
        is set.

        :param topic_handlers: A mapping of topics to their associated handler
        functions.
        """
        try:
            self.consumer.subscribe(list(topic_handlers.keys()))
            while not self.terminate_event or not self.terminate_event.is_set():
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error("Consumer error: {}".format(msg.error()))
                logger.info(
                    f"Message received: {msg.value().decode('utf-8')} \
                        topic {msg.topic()}"
                )
                call_handlers(topic_handlers, msg)
        finally:
            self.consumer.close()
