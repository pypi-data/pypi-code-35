"""Unit tests the project methods of the Matchlight SDK."""
import datetime
import json

import pytest
import responses
import six.moves

import matchlight


PROJECT_TYPES = ('document', 'pii', 'source_code')


def test_project_last_modified(project):
    """Verifies that a project's ``last_date_modified`` is parsed."""
    assert project.last_modified == datetime.datetime.fromtimestamp(
        project.last_date_modified)


@responses.activate
def test_project_add(connection, project_name, project_payload,
                     project_type, upload_token):
    """Verifies project creation."""
    responses.add(
        method=responses.POST,
        url='{}/project/add'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'data': project_payload},
        status=200
    )
    project = connection.projects.add(project_name, project_type)
    assert project.upload_token == upload_token
    assert len(responses.calls) == 1


@responses.activate
def test_project_edit(connection, project, project_payload):
    """Verifies project renaming."""
    responses.add(
        method=responses.POST,
        url='{}/project/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token,
        ),
        json='{}',
        status=200
    )
    new_name = 'Test Project 1'
    connection.projects.edit(project, new_name)
    assert project.name == new_name
    assert len(responses.calls) == 1

    new_name = 'Test Project 2'
    responses.add(
        method=responses.GET,
        url='{}/project/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token,
        ),
        json=project_payload,
        status=200
    )
    project = connection.projects.edit(project, new_name)
    assert project.name == new_name
    assert len(responses.calls) == 2


@responses.activate
def test_project_delete(connection, project, project_payload):
    """Verifies project deletion."""
    responses.add(
        method=responses.POST,
        url='{}/project/{}/delete'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token,
        ),
        json='{}',
        status=200
    )
    # responses.add(
    #     method=responses.GET,
    #     url='{}/project/{}'.format(
    #         matchlight.MATCHLIGHT_API_URL_V2,
    #         project.upload_token,
    #     ),
    #     json=project_payload,
    #     status=200
    # )
    connection.projects.delete(project)
    assert len(responses.calls) == 1


@responses.activate
def test_project_filter(connection, project_payload, project):
    """Verifies project listing and filtering by type."""
    responses.add(
        method=responses.GET,
        url='{}/projects'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'data': [project_payload]},
        status=200
    )
    projects = connection.projects.filter()
    assert len(projects) == 1
    assert projects[0].upload_token == project.upload_token
    assert len(responses.calls) == 1

    project_list = [project_payload]
    for _ in six.moves.range(5):
        payload = project_payload.copy()
        for project_type in PROJECT_TYPES:
            if project_type == payload['project_type']:
                continue
            payload['project_type'] = project_type
            break
        project_list.append(payload)
    responses.add(
        method=responses.GET,
        url='{}/projects'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'data': project_list},
        status=200
    )
    projects = connection.projects.filter(project_type=project.project_type)
    assert len(projects) == 1
    assert projects[0].project_type == project.project_type
    assert len(responses.calls) == 2


@responses.activate
def test_project_get(connection, project_payload, project):
    """Verifies project retrieval."""
    responses.add(
        method=responses.GET,
        url='{}/project/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        body=json.dumps(project_payload),
        status=200
    )
    responses.add(
        method=responses.GET,
        url='{}/project/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        body='{}',
        status=404
    )
    responses.add(
        method=responses.GET,
        url='{}/project/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        body='{}',
        status=500
    )

    project_ = connection.projects.get(project.upload_token)
    assert project.upload_token == project_.upload_token
    assert len(responses.calls) == 1

    project_ = connection.projects.get(project.upload_token)
    assert project_ is None
    assert len(responses.calls) == 2

    with pytest.raises(matchlight.error.APIError):
        connection.projects.get(project.upload_token)
    assert len(responses.calls) == 3


@responses.activate
def test_project_iteration(connection, project, project_payload):
    """Verifies project iteration."""
    responses.add(
        method=responses.GET,
        url='{}/projects'.format(matchlight.MATCHLIGHT_API_URL_V2),
        json={'data': [project_payload]},
        status=200,
    )
    projects_iterable = iter(connection.projects)
    assert next(projects_iterable).details == project.details
    with pytest.raises(StopIteration):
        next(projects_iterable)
    assert len(responses.calls) == 1
