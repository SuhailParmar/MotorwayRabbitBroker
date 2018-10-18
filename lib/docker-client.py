import docker


class DockerClient:

    def __init__(self):
        self.host = "localhost"
        self.client = docker.client.from_env()
        self.running_container_ids = []

    def create_rabbit_container(self):
        rabbit_port = {'15672/tcp': 15672, '5672/tcp': 5672}

        has_created = self.client.containers.run(
            "rabbitmq:3.7-management", name="mq",
            ports=rabbit_port, detach=True)

        print(has_created.id)
        return has_created

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
        return False


if __name__ == '__main__':
    d = DockerClient()
    if d.create_rabbit_container():
        print('Created Rabbit')
    d.kill_rabbit_container()
