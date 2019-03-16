# -*- coding: utf-8 -*-
"""This module is used to use the GitLab API to automatically create a MR for a specific project, assigned to you.
This Python library is intended to be used by in a Docker image in the GitLab CI. Hences lots of the cli options can
also be environment variables, most of which will be provided with the GitLab CI. However this package allows you
to do this using the CLI if you so wish.

Example:
    ::

        $ pip install -e .
        $ gitlab_auto_mr --private-token xxx --source-branch feature --project-id 11121006 \
                         --project-url https://gitlab.com/hmajid2301 --user-id 2902137

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import re
import sys

import requests
import click


"""Acts as the main function is called by when you use `gitlab_auto_mr`.

* It checks if the source branch is the target branch
* It checks if the MR already exists for that target onto the source
* It then creates the MR
* Finally it updates the MR which extra attributes i.e. Squash commits or Auto Merge etc.

Args:
    private_token (str): Private GITLAB token, used to authenticate when calling the MR API.
    source_branch (str): The source branch to merge into..
    project_id (int): The project ID on GitLab to create the MR for.
    project_url (str): The project URL on GitLab to create the MR for.
    user_id (int): The GitLab user ID to assign the created MR to.
    target_branch (str): The target branch to merge onto, i.e. master.
    commit_prefix (str): Prefix for the MR title i.e. WIP.
    remove_branch (bool): Set to True if you want the source branch to be removed after MR
    squash_commits (bool): Set to True if you want commits to be squashed.
    description (str): Description in the MR.

"""


@click.command()
@click.option('--private-token', envvar='GITLAB_PRIVATE_TOKEN', required=True,
              help="Private GITLAB token, used to authenticate when calling the MR API.")
@click.option('--source-branch', envvar='CI_COMMIT_REF_NAME', required=True,
              help="The source branch to merge into.")
@click.option('--project-id', envvar='CI_PROJECT_ID', required=True, type=int,
              help="The project ID on GitLab to create the MR for.")
@click.option('--project-url', envvar='CI_PROJECT_URL', required=True,
              help="The project URL on GitLab to create the MR for.")
@click.option('--user-id', envvar='GITLAB_USER_ID', required=True, type=int,
              help="The GitLab user ID to assign the created MR to.")
@click.option('--target-branch', envvar='TARGET_BRANCH',
              help="The target branch to merge onto.")
@click.option('--commit-prefix', envvar='COMMIT_PREFIX', default="WIP",
              help="Prefix for the MR title i.e. WIP.")
@click.option('--remove-branch', envvar='REMOVE_BRANCH', type=bool, default=False,
              help="Set to True if you want the source branch to be removed after MR.")
@click.option('--squash-commits', envvar='SQUASH', type=bool, default=False,
              help="Set to True if you want commits to be squashed.")
@click.option('--description', envvar='DESCRIPTION',
              help="Description in the MR.")
def cli(private_token, source_branch, project_id, project_url, user_id, target_branch, commit_prefix, remove_branch,
        squash_commits, description):
    try:
        url = get_api_url(project_id, project_url)
        commit_title = get_mr_title(commit_prefix, source_branch)
        headers = {"PRIVATE-TOKEN": private_token}
        target_branch = get_target_branch(headers, target_branch, url)

        check_if_source_is_target(source_branch, target_branch)
        response = make_api_call(f"{url}/merge_requests?state_opened", headers=headers)
        check_if_mr_exists(response, source_branch)

        data = {
            "id": project_id,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "remove_source_branch": remove_branch,
            "squash": squash_commits,
            "title": commit_title,
            "assignee_id": user_id,
            "description": description,
        }
        make_api_call(method="post", url=f"{url}/merge_requests", headers=headers, data=data)
        print(f"Created a new MR {commit_title}, assigned to you.")
    except SystemError:
        sys.exit(1)


def get_api_url(project_id, project_url):
    """Gets the url (base name) i.e. gitlab.com or a private gitlab instance to make the API call to. The full API path
    would be {host}/api/v4/projects

    Args:
        project_id (int): The project ID on GitLab to create the MR for.
        project_url (str): The project URL on GitLab to create the MR for.

    Returns:
        str: The base url name i.e. gitlab.com

    """
    host = re.search("^https?://[^/]+", project_url).group(0)
    url = f"{host}/api/v4/projects/{project_id}"
    return url


def check_if_source_is_target(source_branch, target_branch):
    """Checks if the target branch and source branch are the same.

    Args:
        source_branch (str): The source branch to merge into..
        target_branch (str): The target branch to merge onto, i.e. master.

    """
    if source_branch == target_branch:
        print("Source Branch and Target branches must be different.")
        print(f"Source: {source_branch}, Target: {target_branch}")
        sys.exit(1)


def check_if_mr_exists(response, source_branch):
    """Checks if an MR for the source branch (i.e. feature/abc) already exists.

    Args:
        response (dict): The json response from API checking which MRs are currently open.
        source_branch (str): The source branch to merge into..

    Raises:
        SystemError: If MR already exists.

    """
    source_branch_mr = [mr for mr in response if mr["source_branch"] == source_branch]
    if source_branch_mr:
        print(f"no new merge request opened, one already exists for this branch {source_branch}.")
        raise SystemError


def get_mr_title(commit_prefix, source_branch):
    """Gets the title of the MR. If a prefix exists we add it to the URL. By default we add a prefix of WIP, so the
    MR doesn't get merged by accident.

    Args:
        commit_prefix (str): Prefix for the MR title i.e. WIP.
        source_branch (str): The source branch to merge into..

    Returns:
        str: Title of the MR we will create .

    """
    commit_title = source_branch
    if commit_prefix:
        commit_title = f"{commit_prefix}: {commit_title}"
    return commit_title


def get_target_branch(headers, target_branch, url):
    """If target branch isn't specified find the default branch and use it as the target branch will typically be
    master.

    Args:
        headers (dict): Headers for the API request.
        target_branch (str): The target branch to merge onto, i.e. master.
        url (str): The url to make the API request to.

    Returns:
        str: The target branch name.

    """
    if not target_branch:
        response = make_api_call(url=url, headers=headers)
        target_branch = response['default_branch']
    return target_branch


def make_api_call(url, method="get", headers=None, data=None):
    """If target branch isn't specified find the default branch and use it as the target branch will typically be
    master.

    Args:
        url (str): The url to make the API request to.
        method (:obj:`str`, optional): The HTTP verb to use. Defaults to get.
        headers (:obj:`dict`, optional): Headers for the API request. Defaults to None.
        data (:obj:`dict`, optional): The body for the API request, Default to None. Will be sent as json.

    Returns:
        dict: The API response (json).

    Raises:
        SystemError: If the API request failed.
    """
    try:
        response = requests.request(method, url=url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {url}")
    except requests.exceptions.Timeout:
        print(f"Timed out connecting to {url}")

    print(f"API request failed to {url}")
    raise SystemError



