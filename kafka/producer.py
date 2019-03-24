import logging
import time
from json import dumps

import confluent_kafka

from kafka import BROKER, TOPIC

logger = logging.Logger(__name__)


def delivery_report(err, msg):
    if err is not None:
        logger.error('Message delivery failed: %s', err)
    else:
        logger.warning('Message: %s, delivered to: %s [%d]', msg.value().decode('utf-8'), msg.topic(), msg.partition())


class Producer(object):
    def __init__(self, conf=None):
        self.conf = conf or {
            'bootstrap.servers': BROKER
        }
        self.producer = confluent_kafka.Producer(**self.conf)

    def send(self, msg):
        self.producer.poll(0)
        data = dumps({'message': msg, 'timestamp': time.time()})
        self.producer.produce(TOPIC, data.encode('utf-8'), callback=delivery_report)
        self.producer.flush()
