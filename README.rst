========
theTrial
========

.. image:: https://img.shields.io/badge/pypi-v0.0.2-green
   :target: https://test.pypi.org/project/the-trial/0.0.2/#description
   :alt: pypi

.. image:: https://img.shields.io/badge/build-passing-%23355E3B
   :target: https://github.com/donMichaelL/theTrial/actions/workflows/main.yaml
   :alt: build

.. image:: https://img.shields.io/badge/License-MIT-blue
   :target: https://github.com/donMichaelL/theTrial/blob/master/LICENSE
   :alt: license

.. image:: https://img.shields.io/badge/pre--commit-enabled-%2300A36C%09
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. image:: https://img.shields.io/badge/Code_Style-black-black?color=black
   :target: https://github.com/psf/black
   :alt: black


``theTrial`` is a microframework designed to provide a simple interface for interacting with Kafka. With a concise and intuitive API, `theTrial` allows you to quickly set up consumers and producers for Kafka topics. Under the hood, it leverages the capabilities of `confluent-kafka <https://github.com/confluentinc/confluent-kafka-python>`_ to ensure efficient and reliable communication with Kafka clusters.


Installation
------------

You can easily install `theTrial` using pip:

.. code-block:: bash

   pip install theTrial

Quick Start
-----------

Here's a simple example to get you started:

.. code-block:: python

    # Importing required models
    from models import MyModel
    from models import Result

    # Importing the main application class from theTrial module
    from theTrial import TheTrial

    # Creating an instance of TheTrial class
    app = TheTrial()


    # Decorating the consumer function to specify the topics it interacts with
    @app.outopic("out_topic")
    @app.intopic("in_topic")
    def consumer(msg: MyModel, topic: str) -> Result:
        """Message processing"""
        # This is where the message processing should take place
        # For now, a placeholder result is returned
        return result


    if __name__ == "__main__":
        # Running the app
        app.run()


In the example above:

- We define a consumer using the ``@app.intopic`` decorator, specifying the topic from which messages will be consumed.
- The consumer processes the message and returns a result.
- The result is then serialized and sent to the "out_topic" topic, as specified by the ``@app.outopic`` decorator.

Additional Information:
^^^^^^^^^^^^^^^^^^^^^^^

- The consumer function can have no arguments, one argument, or two arguments.
- The first argument (if exists) is the Kafka message received, which has been deserialized and is provided as an instance of the Pydantic Model used for type hints.
- The second argument (if exists) is the topic.

Models with Pydantic
--------------------

All models in `theTrial` should be defined using `Pydantic <https://docs.pydantic.dev/latest/>`_. This means you can leverage all the features of Pydantic, including data validation and more.

.. note::
   If you intend to use any of these models, please ensure you have Pydantic installed by running `pip install    pydantic`.

Settings Configuration
----------------------

``theTrial`` utilizes an environment variable, ``SETTINGS_MODULE``, to determine the location of the settings module. If this environment variable is not defined, the framework will, by default, search the current path for a module named ``settings.py``.

Inside the ``settings.py`` module, users are expected to define two key variables:

1. ``CONFIG_CONSUMER``: This should contain the configuration details for Kafka's consumer.
2. ``CONFIG_PRODUCER``: This should contain the configuration details for Kafka's producer.

Example ``settings.py``:

.. code-block:: python

    # Kafka Consumer Configuration
    CONFIG_CONSUMER = {
        "bootstrap_servers": "localhost:9092",
        "group_id": "my-group",
        "auto_offset_reset": "earliest"
        # ... other Kafka consumer settings ...
    }

    # Kafka Producer Configuration
    CONFIG_PRODUCER = {
        "bootstrap_servers": "localhost:9092",
        # ... other Kafka producer settings ...
    }

For a detailed explanation and additional configuration options, refer to the official Confluent documentation: `Confluent Kafka Python Documentation <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html>`_.

User-Defined Settings
^^^^^^^^^^^^^^^^^^^^^

In addition to the predefined settings, users can define their own custom settings within the ``settings.py`` module. This allows for flexibility and extensibility tailored to specific application needs.

To ensure consistency and avoid potential conflicts, all user-defined settings should be in UPPERCASE. For example:

.. code-block:: python

    MY_CUSTOM_SETTING = "SomeValue"

You can then retrieve this setting in your application by importing it:

.. code-block:: python

    from settings import MY_CUSTOM_SETTING

Logging Configuration
---------------------

``theTrial`` employs and extends Python's built-in logging module for system logging. The configuration for logging is driven by the environmental variable ``CONFIG_LOGGING``.

To customize logging, including adding your own log handlers or any other logging configurations, you should define a ``CONFIG_LOGGING`` dictionary in your `settings.py` module.

Example `settings.py`:

.. code-block:: python

    CONFIG_LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }

Remember to structure the ``CONFIG_LOGGING`` dictioWnary according to the structure expected by Python's logging config module. Refer to the official `Python logging documentation <https://docs.python.org/3/library/logging.config.html>`_ for more details on logging configurations.


CLI Commands
------------

``theTrial`` also comes with a set of CLI commands to help you set up and manage your projects:

Start Command
^^^^^^^^^^^^^

To initialize a new project structure, use the `start` command:

.. code-block:: bash

   theTrial start --name [YOUR_APP_NAME]

By default, the main app file will be named `app.py`. You can specify a different name using the ``--name`` option.

This command will:

- Create the main app file (`[YOUR_APP_NAME].py`).
- Set up a ``settings.py`` file with default Kafka configurations.
- Create a ``models/`` directory with an ``__init__.py`` and a ``models.py`` file for defining your Pydantic models.
