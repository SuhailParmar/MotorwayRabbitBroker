import docker
import logging
from sys import exit
from time import sleep
docker_logger = logging.getLogger("DockerClient")


class DockerClient:

    def __init__(self):
        self.host = "localhost"
        self.client = docker.client.from_env()
        self.running_container_ids = []

    def create_rabbit_container(self, image, port, management_port):
        rabbit_port = {'15672/tcp': management_port, '5672/tcp': port}

        docker_logger.info("Creating Rabbit Mq...")

        try:
            has_created = self.client.containers.run(
                image, name="mq", ports=rabbit_port, detach=True)
        except docker.errors.APIError:
            docker_logger.error(
                "Couldn't create rabbit container, stop/remove the existing one. ${docker rm $(docker ps -aq) }")
            exit(1)
        except Exception as e:
            docker_logger.error(e)
            exit(1)

        docker_logger.debug(has_created.id)
        sleep(10)  # TODO implement Wait for it
        docker_logger.info("Rabbit Mq is Up!")
        return True

    def kill_rabbit_container(self):
        running_containers = self.client.containers.list()
        for container in running_containers:
            if container.attrs["Name"] == "/mq":
                try:
                    container.stop()
                    container.remove(force=True)
                    return True
                except Exception as e:
                    print(e)
        exit(1)


if __name__ == "__main__":
    d = DockerClient()
    d.kill_rabbit_container()
