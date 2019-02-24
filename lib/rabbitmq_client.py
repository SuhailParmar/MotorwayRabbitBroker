import pika
import logging
import requests
from sys import exit
from subprocess import call

import lib.rabbit_config as config
mq_logger = logging.getLogger("RabbitMqClient")


class RabbitMQClient:

    def __init__(self):
        self.username = config.rabbit_username
        self.password = config.rabbit_password
        self.host = config.rabbit_host
        self.port = config.rabbit_port
        self.mport = config.rabbit_mport
        self.exchange = config.rabbit_exchange
        self.vhost = config.rabbit_vhost

    def bind_queue_to_exchange(self, channel, queue, routing_key):
        """
        channel - Can be extracted from the connection
        queue   - Once a queue is declared
        """

        try:
            channel.queue_bind(queue=queue, exchange=self.exchange,
                               routing_key=routing_key)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to bind queue:{0} to exchange:{1} with RK: {2}".format(
                queue, (self.exchange), routing_key))
            exit(1)

        mq_logger.info("Successfully bound queue: {0} to exchange: {1} with RK: {2}".format(
            queue, (self.exchange), routing_key))
        return

    def connect_to_mq(self):
        mq_logger.debug('Connecting to mq...')
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        try:
            #connection = pika.ConnectionParameters(host=self.host, port=int(self.port), virtual_host=self.vhost, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            mq_logger.info('Successfully connected to rabbit!')
        except Exception as e:
            mq_logger.error(e)
            exit(1)

        return connection

    def declare_queue(self, channel, queue):
        """
        If the queue doesn't exists create it and
        bind to to an exchange
        """
        try:
            channel.queue_declare(queue=queue)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error("Unable to declare queue:{}".format(queue))
            exit(1)
        mq_logger.info("Successfully declared queue: {}".format(queue))

    def declare_exchange(self, channel):
        """
        If an exchange doesn't exist create it
        """
        try:
            channel.exchange_declare(exchange=self.exchange)
        except Exception as e:
            mq_logger.error(e)
            mq_logger.error(
                "Unable to declare exchange:{}".format(self.exchange))
            exit(1)
        mq_logger.info(
            "Successfully declared exchange: {}".format(self.exchange))

    def declare_vhost(self):

        response_code = call(["./bin/create_vhost.bash",
                              # Pass credentials as shell args
                              "{}".format(self.username),
                              "{}".format(self.password),
                              "{}".format(self.host),
                              "{}".format(self.mport),
                              "{}".format(self.vhost)])
        if response_code != 0:
            mq_logger.error("Failed to create vHost: {}".format(self.vhost))
            exit(1)

        print("Successfully created vHost: {}".format(self.vhost))
        return True
