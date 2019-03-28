# -*- coding: utf-8 -*-

from datetime import datetime
import json
import getpass
import os
import sys
from fabric import Connection, Config, transfer
from github import Github
from github.GithubException import UnknownObjectException


#################################### Prepare deploy script ##########################################


def get_absolute_path(relative_path):
    """
    :param relative_path: relative path of the file to the current directory of auto.py file
    :return:
    """
    # current directory path that contain this file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return "{0}/{1}".format(dir_path, relative_path)




def check_valid_repo_info(repo_name, tag_name, git_access_token):
    g = Github(git_access_token)
    try:
        repo = g.get_user('Magestore').get_repo(repo_name)
        tags = repo.get_tags()
        return any(tag.name == tag_name for tag in tags)
    except UnknownObjectException as e:
        print(e)
        return False


def update_deploy_script(repo_name, tag_name, github_access_token, instance_info):
    package_file_name = '{tag_name}.tar.gz'.format(tag_name=tag_name)
    raw_deploy_file_path = get_absolute_path('data/raw_deploy.sh')
    deploy_file_path = get_absolute_path('data/deploy.sh')

    with open(raw_deploy_file_path, 'r') as f:
        content = f.read()
        content = content.replace("<access_token>", github_access_token)
        content = content.replace("<repo_name>", repo_name)
        content = content.replace("<package_file_name>", package_file_name)
        content = content.replace("<source_folder>", instance_info.get("source_folder"))
        content = content.replace("<web_container_id>", instance_info.get("web_container_id"))

    with open(deploy_file_path, 'w') as f:
        f.write(content)


def update_install_prerequisite(remote_user, remote_group):
    install_prerequisite_path = get_absolute_path('data/install_prerequisite.sh')
    raw_install_prerequisite_path = get_absolute_path('data/raw_install_prerequisite.sh')

    with open(raw_install_prerequisite_path) as f:
        content = f.read()
        content = content.replace('<remote_user>', remote_user)
        content = content.replace('<remote_group>', remote_group)

    with open(install_prerequisite_path, 'w') as f:
        f.write(content)


################################# Deploy new released package to demo server #######################################

def get_connection(host, user, su_pass='', key_path=''):
    if key_path:
        c = Connection(host, user, connect_kwargs={'key_filename': key_path})
    else:
        config = Config(overrides={'sudo': {'password': su_pass, "prompt": "[sudo] password: \n"}})
        c = Connection(host, user, connect_kwargs={"password": su_pass}, config=config)
    return c


def get_current_time():
    current_time = '{:%H%M%S_%d%m%Y}'.format(datetime.today())
    return current_time


def send_files_to_remote_server(connection, source_path, dest_path):
    """
    :param connection: connection to remote server
    :param source_path: path to file on local server
    :param dest_path: path to folder will be contain file on remote server
    :return: None
    """
    transfer_obj = transfer.Transfer(connection)
    transfer_obj.put(source_path, dest_path)


def install_prerequisite_remote_server(connection):
    local_install_prerequisite_path = get_absolute_path('data/install_prerequisite.sh')
    remote_user = connection.run('echo $USER').stdout.replace('\n', '')
    remote_group = connection.run('echo $GROUP').stdout.replace('\n', '')
    update_install_prerequisite(remote_user, remote_group)
    remote_install_prerequisite_path = '/tmp/tmp-install-file-{0}'.format(get_current_time())
    connection.run('mkdir -p {0}'.format(remote_install_prerequisite_path))
    send_files_to_remote_server(connection, local_install_prerequisite_path, remote_install_prerequisite_path)
    connection.sudo('bash {0}/install_prerequisite.sh'.format(remote_install_prerequisite_path))
    connection.run('rm -rf {0}'.format(remote_install_prerequisite_path))


def deploy(repo_name, tag_name, github_access_token, instance_info):
    connection = get_connection(
        host=instance_info.get('ip'),
        user=instance_info.get('user'),
        su_pass=instance_info.get('password'),
        key_path=instance_info.get('local_key_file_path')
    )

    install_prerequisite_remote_server(connection)

    # reset connection
    connection = get_connection(
        host=instance_info.get('ip'),
        user=instance_info.get('user'),
        su_pass=instance_info.get('password'),
        key_path=instance_info.get('local_key_file_path')
    )

    update_deploy_script(repo_name, tag_name, github_access_token, server_info)
    local_deploy_file_path = get_absolute_path('data/deploy.sh')
    remote_deploy_file_path = '/tmp/tmp-deploy-file-{0}'.format(get_current_time())
    connection.run('mkdir -p {0}'.format(remote_deploy_file_path))
    send_files_to_remote_server(connection, local_deploy_file_path, remote_deploy_file_path)
    connection.run('bash {0}/deploy.sh'.format(remote_deploy_file_path))
    connection.run('rm -rf {0}'.format(remote_deploy_file_path))
