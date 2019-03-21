import docker


class DockerModulo:

    def __init__(self):
        self.client = docker.from_env()

    def lista_conteiner(self):
        return lista_conteiner =  self.client.containers.list(all=True)

        