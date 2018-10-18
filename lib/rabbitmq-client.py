import pika
import logging
import queue
from functools import partial
from json import dumps, loads
from sys import exit
import lib.config as config

mq_logger = logging.getLogger("RabbitMqClient")


class RabbitMQClient:

    def __init__(self):
        self.username = config.rabbit_username
        self.password = config.rabbit_password
        self.host = config.rabbit_host
        self.port = config.rabbit_port
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.vhost = config.rabbit_vhost

    def bind_queue_to_exchange(self, channel, queue,
                               rk=config.rabbit_routing_key):
        """
        channel - Can be extracted from the connection
        queue   - Once a queue is declared
        """

        try:
            channel.queue_bind(queue=queue, exchange=self.exchange,
                               routing_key=rk)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to bind queue:{0} to exchange:{1} with RK: {2}".format(
                queue, (self.exchange), rk))
            exit(1)

        mq_logger.info("Successfully bound queue: {0} to exchange: {1} with RK: {2}".format(
            queue, (self.exchange), rk))
        return

    def connect_to_mq(self):
        mq_logger.debug('Connecting to mq...')
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        try:
            connection = pika.BlockingConnection(parameters)
            mq_logger.info('Successfully connected to rabbit!')
        except Exception as e:
            mq_logger.error(e)
            exit(1)

        return connection

    def declare_queue(self, channel, queue_name=config.rabbit_queue):
        """
        If the queue doesn't exists create it and
        bind to to an exchange
        """
        try:
            channel.queue_declare(queue=queue_name)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to declare queue:{}".format(queue_name))
            exit(1)
        mq_logger.info("Successfully declared queue: {}".format(queue_name))
