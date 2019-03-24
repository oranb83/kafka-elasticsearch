import logging
from json import loads

import confluent_kafka

from kafka import BROKER, TOPIC

logger = logging.Logger(__name__)


class Consumer(object):
    def __init__(self, conf=None):
        self.conf = conf or {
            'bootstrap.servers': BROKER,
            'group.id': 'connect',
            'auto.offset.reset': 'latest'
        }
        self.consumer = confluent_kafka.Consumer(**self.conf)
        self.consumer.subscribe([TOPIC])

    def get(self):
        # I'm using a loop in case some messages got stack in Kafka,
        # this is a rare case affected by issues with the kafka broker terminating unexpectedly.
        messages = []
        running = True
        while running:
            msg = self.consumer.poll()
            if msg is None:
                return messages
            if msg.error():
                if msg.error().str() != 'Broker: No more messages':
                    logger.error('Consumer error: %s', msg.error())
                return messages

            msg = loads(msg.value().decode('utf-8'))
            logger.warning('Received message: %s', msg)
            messages.append(msg)

        return messages
