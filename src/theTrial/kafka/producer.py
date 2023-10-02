from typing import Optional

from confluent_kafka import Producer

from . import logger
from ..settings import load_settings as settings


class KafkaProducer:
    """
    A simple Kafka producer class for sending messages to Kafka topics.

    This class wraps the basic functionality of the Confluent Kafka Producer,
    providing a straightforward interface for producing messages with delivery
    callbacks.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the KafkaProducer instance.
        If a configuration dictionary is provided, it will be used to configure
        the Kafka producer.
        If not, the default configuration from settings.CONFIG_PRODUCER will be used.


        :param config: Configuration dictionary for the Kafka producer.
        """
        config = config or settings.CONFIG_PRODUCER  # type: ignore
        self.producer = Producer(config)

    def send_message(self, topic: str, msg: str) -> None:
        """
        Send a message to the specified Kafka topic.

        :param topic: The name of the Kafka topic to which the message should be sent.
        :param msg: The message to be sent to the Kafka topic.
        """

        def _acked(err, msg):
            if err is not None:
                logger.error(f"Failed to deliver message: {str(msg)}: {str(err)}")
            else:
                logger.info(f"Message produced: {str(msg.value())}")

        self.producer.produce(topic, value=msg, callback=_acked)
        self.producer.flush()
