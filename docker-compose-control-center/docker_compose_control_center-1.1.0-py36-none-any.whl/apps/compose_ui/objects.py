from datetime import datetime
from types import SimpleNamespace
from typing import List, TextIO, Optional

from django.conf import settings
from django.utils.dateparse import parse_datetime
from docker.models.containers import Container as DockerContainer
from pytz import utc

from control_center.apps.compose_ui import docker


class ComposeServiceConfig(object):
    def __init__(self, config: dict, service_name: str, service_hash: str):
        self._config: dict = config
        self.service_name: str = service_name
        self.hash = service_hash
        self.image: str = config.get("image")
        self.container_name: str = config.get("container_name")
        self.restart: str = config.get("restart")
        self.scale: int = self.get_scale(config)
        self.volumes: List[str] = config.get("volumes")
        self.ports: List[str] = config.get("ports")
        self.environment: dict = config.get("environment")
        self.depends_on: List[str] = config.get("depends_on")
        self.links: List[str] = config.get("links")

    def merged_dependencies(self) -> List[str]:
        return list(set(self.depends_on) | set(self.links))

    @staticmethod
    def get_scale(config: dict) -> int:
        if config:
            if "scale" in config.keys():
                return config["scale"]
            elif "deploy" in config.keys():
                return config["deploy"].get("replicas")
        return 1


class ComposeProjectConfig(object):
    def __init__(self, original_file: TextIO, config: dict, project_name: str):
        self._file: TextIO = original_file
        self._config: object = config
        self.project_name: str = project_name
        self.version: float = float(config["version"])
        service_hash_dict = docker.service_hashes(project_name=project_name)
        self.service_configs: List[ComposeServiceConfig] = []
        for service_name in config["services"]:
            self.service_configs.append(
                ComposeServiceConfig(
                    config=config["services"][service_name],
                    service_name=service_name,
                    service_hash=service_hash_dict[self.project_name][service_name],
                )
            )

    def service_config(self, project_name: str, service_name: str):
        if project_name == self.project_name:
            return next(filter(lambda ser_conf: ser_conf.service_name == service_name, self.service_configs))


class Container(object):
    STATUS = SimpleNamespace(
        **{
            "CREATED": "created",
            "RESTARTING": "restarting",
            "RUNNING": "running",
            "REMOVING": "removing",
            "PAUSED": "paused",
            "EXITED": "exited",
            "DEAD": "dead",
        }
    )

    def __init__(self, container: DockerContainer):
        self._docker_container: DockerContainer = container
        self.name: str = container.name
        self.short_id: str = container.short_id
        self.id: str = container.id
        self.tags: str = container.image.tags
        self.status: str = container.status
        self.started_at: datetime = parse_datetime(container.attrs["State"]["StartedAt"]) if parse_datetime(
            container.attrs["State"]["StartedAt"]
        ) != utc.localize(datetime.min) else None
        self.service: str = container.labels.get("com.docker.compose.service")
        self.service_hash: str = container.labels.get("com.docker.compose.config-hash")
        self.project: str = container.labels.get("com.docker.compose.project")

    def tags_display(self) -> str:
        tags_joined = "\n".join(self.tags)
        return remove_custom_registry_from_image_name(tags_joined) if self.tags else tags_joined

    def can_be_stopped(self) -> bool:
        return self.status == self.STATUS.RUNNING

    def can_be_started(self) -> bool:
        return self.status == self.STATUS.EXITED

    def can_be_restarted(self):
        return self.status == self.STATUS.RUNNING

    def can_be_removed(self):
        return self.status == self.STATUS.EXITED

    def stop(self):
        self._docker_container.stop()

    def start(self):
        self._docker_container.start()

    def restart(self):
        self._docker_container.restart()

    def rm(self):
        self._docker_container.remove()

    def rename(self, name: str):
        self._docker_container.rename(name)


class ComposeService(object):
    ROLLBACK_SUFFIX = "_previous"

    def __init__(self, service_name: str, project_name: str, service_config: Optional[ComposeServiceConfig]):
        self.service_name: str = service_name
        self.project_name: str = project_name
        self.config: Optional[ComposeServiceConfig] = service_config
        self.containers: List[Container] = []
        self.refresh_containers()

    def refresh_containers(self):
        self.containers = docker.containers_for_service(project_name=self.project_name, service_name=self.service_name)

    def stopped_containers(self) -> List[Container]:
        return list(filter(lambda cont: cont.status == Container.STATUS.EXITED, self.containers))

    def running_containers(self) -> List[Container]:
        return list(filter(lambda cont: cont.status == Container.STATUS.RUNNING, self.containers))

    def rollback_containers(self) -> List[Container]:
        return list(filter(lambda cont: cont.name.endswith(self.ROLLBACK_SUFFIX), self.containers))

    def out_of_sync_containers(self) -> List[Container]:
        return list(filter(lambda cont: self.config and cont.service_hash != self.config.hash, self.containers))

    def config_image_display(self) -> str:
        return remove_custom_registry_from_image_name(self.config.image) if self.config else ""

    def can_be_upped(self) -> bool:
        return not any(self.rollback_containers())

    def can_be_started(self) -> bool:
        return not any(self.rollback_containers()) and any(self.stopped_containers())

    def can_be_stopped(self) -> bool:
        return any(self.running_containers())

    def can_be_restarted(self) -> bool:
        return not any(self.rollback_containers()) and any(self.containers)

    def can_be_removed(self) -> bool:
        return any(self.stopped_containers())

    def can_be_updated(self) -> bool:
        return (
            self.config
            and not self.config.ports
            and any(filter(lambda cont: cont not in self.rollback_containers(), self.out_of_sync_containers()))
        )

    def can_be_rolled_back(self) -> bool:
        return any(self.rollback_containers())

    def up(self):
        docker.pull_image(self.config.image)
        docker.execute_compose_command(self.project_name, ["up", "--detach", "--no-deps", self.service_name])

    def stop(self):
        docker.execute_compose_command(self.project_name, ["stop", self.service_name])

    def start(self):
        docker.execute_compose_command(self.project_name, ["start", self.service_name])

    def rm(self):
        docker.execute_compose_command(self.project_name, ["rm", "--force", self.service_name])

    def restart(self):
        docker.execute_compose_command(self.project_name, ["restart", self.service_name])

    def scale(self, scale):
        docker.pull_image(self.config.image)
        docker.execute_compose_command(
            self.project_name,
            [
                "up",
                "--detach",
                "--no-deps",
                "--scale",
                f"{self.service_name}={scale}",
                "--no-recreate",
                self.service_name,
            ],
        )

    def update(self):
        docker.pull_image(self.config.image)
        # remove previous rollback containers
        for container in self.rollback_containers():
            container.rm()
        self.refresh_containers()
        # rename current containers
        for container in self.containers:
            new_name = container.name + self.ROLLBACK_SUFFIX
            container.rename(new_name)
        self.refresh_containers()
        # scale
        self.scale(self.config.scale * 2)
        # stop old containers
        for container in self.rollback_containers():
            container.stop()

    def rollback(self):
        rollback_containers = self.rollback_containers()
        for container in self.containers:
            if container not in rollback_containers:
                container.stop()
                container.rm()
            elif container in rollback_containers:
                container.rename(container.name.replace(self.ROLLBACK_SUFFIX, ""))
                container.start()


class ComposeProject(object):
    def __init__(
        self, project_name: str, project_config: ComposeProjectConfig = None, services: List[ComposeService] = None
    ):
        self.project_name: str = project_name
        self.config: ComposeProjectConfig = project_config
        self.services: List[ComposeService] = [] if services is None else services

    def stopped_containers(self) -> List[Container]:
        return [container for sublist in self.services for container in sublist.stopped_containers()]

    def running_containers(self) -> List[Container]:
        return [container for sublist in self.services for container in sublist.running_containers()]

    def rollback_containers(self) -> List[Container]:
        return [container for sublist in self.services for container in sublist.rollback_containers()]

    def can_be_upped(self) -> bool:
        return not any(self.rollback_containers())

    def can_be_downed(self) -> bool:
        return True

    def can_be_removed(self) -> bool:
        return not any(self.rollback_containers()) and any(self.stopped_containers())

    def can_be_restarted(self) -> bool:
        return not any(self.rollback_containers()) and (
            any(self.stopped_containers()) or any(self.running_containers())
        )

    def up(self):
        for service in self.services:
            docker.pull_image(service.config.image)
        docker.execute_compose_command(self.project_name, ["up", "--detach"])

    def down(self):
        docker.execute_compose_command(self.project_name, ["down"])

    def rm(self):
        docker.execute_compose_command(self.project_name, ["rm", "--force"])

    def restart(self):
        docker.execute_compose_command(self.project_name, ["restart"])


def remove_custom_registry_from_image_name(name: str) -> str:
    return name.replace(settings.STRIP_CUSTOM_REGISTRY, "")
