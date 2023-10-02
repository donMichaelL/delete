from collections import defaultdict
from collections.abc import Callable
from functools import wraps
from threading import Event
from threading import Thread

from .kafka.consumer import KafkaConsumer
from .kafka.producer import KafkaProducer


class TheTrial:
    """
    The `TheTrial` class provides an interface for managing Kafka producers
    and consumers. It allows for registering functions to specific Kafka topics,
    so that when a message is received on a topic, the associated function(s)
    are triggered.It is responsible for sending messages to Kafka topics after
    processing data. It manages the lifecycle of a Kafka consumer in a separate thread.

    Decorators:
    - intopic: Register a function to a specific Kafka topic.
    - outopic: Send the result of a function to a specific Kafka topic.
    """

    def __init__(self, **kwargs):
        self.consumer_map = defaultdict(list)
        self.producer = KafkaProducer()
        self.terminate_event = Event()

    def add_function(self, topic, func: Callable) -> None:
        """
        Add a function to the consumer map for a given topic.

        :param topic: The Kafka topic.
        :param func: The function to be executed for the given topic.
        """
        self.consumer_map[topic].append(func)

    def intopic(self, topic: str) -> Callable:
        """
        Decorator to register a function to a specific Kafka topic.

        :param topic: The Kafka topic.
        :return: The decorated function.
        """

        def decorator(func: Callable) -> Callable:
            self.add_function(topic, func)

            @wraps(func)
            def _wrapper(*args, **kwargs):
                pass

            return _wrapper

        return decorator

    def outopic(self, topic: str, **options) -> Callable:
        """
        Decorator to send the result of a function to a specific Kafka topic.

        :param topic: The Kafka topic.
        :param options: Additional options for the decorator.
        :return: The decorated function.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def _wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.producer.send_message(topic=topic, msg=result.json())

            return _wrapper

        return decorator

    def stop(self) -> None:
        """
        Set the termination event, signaling the consumer to stop.
        """
        self.terminate_event.set()

    def run(self) -> None:
        """
        Start the Kafka consumer in a separate thread.
        """
        consumer = KafkaConsumer()
        consumer_thread = Thread(target=consumer.consume, args=(self.consumer_map,))
        consumer_thread.start()
