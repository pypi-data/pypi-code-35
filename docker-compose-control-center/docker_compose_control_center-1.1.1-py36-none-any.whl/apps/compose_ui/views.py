import time
from subprocess import CalledProcessError
from typing import Dict

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from docker.errors import NotFound
from pkg_resources import get_distribution, DistributionNotFound

from control_center.apps.compose_ui import docker
from control_center.apps.compose_ui.decorators import view_has_perm_from_arg
from control_center.apps.compose_ui.objects import ComposeProject, ComposeService, Container


def app_version() -> str:
    try:
        return get_distribution("docker_compose_control_center").version
    except DistributionNotFound:
        # package is not installed
        pass


base_context = {
    "title": settings.SITE_TITLE,
    "auto_refresh": settings.AUTO_REFRESH,
    "disable_container_actions": settings.DISABLE_SERVICE_CONTAINER_ACTIONS,
    "static_version": int(round(time.time() * 1000)),
    "app_version": app_version(),
}


def context(items: Dict) -> Dict:
    return {**base_context, **items}


@login_required
def managed_containers(request):
    compose_config = docker.compose_config()
    cxt = context(
        {
            "project_list": docker.project_list(
                docker.containers_for_project(compose_config.project_name), config=compose_config
            )
        }
    )
    return render(request, "compose_ui/project_containers.html", cxt)


@login_required
def other_project_containers(request):
    compose_config = docker.compose_config()
    cxt = context(
        {
            "project_list": docker.project_list(
                docker.containers_for_project(exclude_project_name=compose_config.project_name)
            )
        }
    )
    return render(request, "compose_ui/project_containers.html", cxt)


@login_required
def standalone_containers(request):
    cxt = context({"container_list": docker.standalone_containers()})
    return render(request, "compose_ui/standalone_containers.html", cxt)


@login_required
def docker_system(request):
    cxt = context({})
    return render(request, "compose_ui/system.html", cxt)


@login_required
@view_has_perm_from_arg("project_name", "up")
def project_up(request, project_name):
    project = ComposeProject(project_name=project_name)
    try:
        project.up()
    except CalledProcessError:
        return HttpResponseServerError("error project up")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("project_name", "down")
def project_down(request, project_name):
    project = ComposeProject(project_name=project_name)
    try:
        project.down()
    except CalledProcessError:
        return HttpResponseServerError("error project down")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("project_name", "restart")
def project_restart(request, project_name):
    project = ComposeProject(project_name=project_name)
    try:
        project.restart()
    except CalledProcessError:
        return HttpResponseServerError("error restarting project")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("project_name", "remove")
def project_rm(request, project_name):
    project = ComposeProject(project_name=project_name)
    try:
        project.rm()
    except CalledProcessError:
        return HttpResponseServerError("error removing stopped containers for project")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "stop")
def service_stop(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.stop()
    except CalledProcessError:
        return HttpResponseServerError("error stopping service")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "start")
def service_start(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.start()
    except CalledProcessError:
        return HttpResponseServerError("error starting service")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "up")
def service_up(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.up()
    except CalledProcessError:
        return HttpResponseServerError("error service up")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "remove")
def service_remove(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.rm()
    except CalledProcessError:
        return HttpResponseServerError("error removing stopped containers for service")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "restart")
def service_restart(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.restart()
    except CalledProcessError:
        return HttpResponseServerError("error restarting service")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "update")
def service_update(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.update()
    except CalledProcessError:
        return HttpResponseServerError("error updating service")
    return redirect_to_referer(request)


@login_required
@view_has_perm_from_arg("service_name", "rollback")
def service_rollback(request, project_name, service_name):
    service = ComposeService(
        project_name=project_name,
        service_name=service_name,
        service_config=docker.compose_config().service_config(project_name=project_name, service_name=service_name),
    )
    try:
        service.rollback()
    except CalledProcessError:
        return HttpResponseServerError("error service rollback")
    return redirect_to_referer(request)


@login_required
def container_stop(request, container_id):
    try:
        container = docker.container_by_id(container_id)
        check_permission_or_deny(user=request.user, container=container, perm="container_stop")
        container.stop()
    except NotFound as error:
        raise Http404(error.explanation)
    except CalledProcessError:
        return HttpResponseServerError("error stopping container")
    except PermissionDenied:
        return HttpResponseForbidden()
    return redirect_to_referer(request)


@login_required
def container_start(request, container_id):
    try:
        container = docker.container_by_id(container_id)
        check_permission_or_deny(user=request.user, container=container, perm="container_start")
        container.start()
    except NotFound as error:
        raise Http404(error.explanation)
    except CalledProcessError:
        return HttpResponseServerError("error starting container")
    except PermissionDenied:
        return HttpResponseForbidden()
    return redirect_to_referer(request)


@login_required
def container_restart(request, container_id):
    try:
        container = docker.container_by_id(container_id)
        check_permission_or_deny(user=request.user, container=container, perm="container_restart")
        container.restart()
    except NotFound as error:
        raise Http404(error.explanation)
    except CalledProcessError:
        return HttpResponseServerError("error restarting container")
    except PermissionDenied:
        return HttpResponseForbidden()
    return redirect_to_referer(request)


@login_required
def container_remove(request, container_id):
    try:
        container = docker.container_by_id(container_id)
        check_permission_or_deny(user=request.user, container=container, perm="container_remove")
        container.rm()
    except NotFound as error:
        raise Http404(error.explanation)
    except CalledProcessError:
        return HttpResponseServerError("error removing container")
    except PermissionDenied:
        return HttpResponseForbidden()
    return redirect_to_referer(request)


@login_required()
@permission_required("docker_system.system_commands", raise_exception=True)
def clean_old_images(request):
    image_ids = docker.execute_docker_command(["images", "--quiet", "--force", "dangling=true"])

    for image_id in image_ids.splitlines():
        command = ["rmi", "--force", str(image_id)]
        docker.execute_docker_command(command)
    return redirect_to_referer(request)


@login_required()
@permission_required("docker_system.system_commands", raise_exception=True)
def prune(request):
    docker.execute_docker_command(["system", "prune", "--force"])
    return redirect_to_referer(request)


@login_required()
@permission_required("docker_system.system_commands", raise_exception=True)
def prune_all(request):
    docker.execute_docker_command(["system", "prune", "--force", "--all"])
    return redirect_to_referer(request)


# Checks whether a user has permission to perform the action on a container; if not, raise PermissionDenied
def check_permission_or_deny(user: User, container: Container, perm: str):
    compose_config = docker.compose_config()
    app_label = None
    if container.project and container.project == compose_config.project_name:
        app_label = container.service
    elif container.project and container.project != compose_config.project_name:
        app_label = "other_projects"
    elif not container.project:
        app_label = "other_containers"
    if not user.has_perm(app_label + "." + perm):
        raise PermissionDenied


def redirect_to_referer(request):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
