from lib.logger import Logger
from lib.docker_client import DockerClient
from lib.rabbitmq_client import RabbitMQClient
from lib.rabbit_config import rabbit_image as image
from lib.rabbit_config import rabbit_port as port
from lib.rabbit_config import rabbit_mport as mport
from lib.rabbit_config import rabbit_queue_definitions as mq_queues
from lib.rabbit_config import rabbit_rk_definitions as mq_rkeys

Logger.initiate_logger()
"""
- Ensure the docker daemon is running.
"""


def main():
    dc = DockerClient()
    dc.create_rabbit_container(image, port, mport)

    mq = RabbitMQClient()
    mq.declare_vhost()
    connection = mq.connect_to_mq()
    channel = connection.channel()
    mq.declare_exchange(channel)

    for i, queue_name in enumerate(mq_queues):
        mq.declare_queue(channel, queue_name)
        mq.bind_queue_to_exchange(channel, queue_name, mq_rkeys[i])


main()
