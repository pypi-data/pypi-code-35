import subprocess
from time import sleep

import click
import requests
import os
import zipfile
import glob
import shutil
import datetime

from oly.utils import Utils, Clr


class BitBucketApi:
    BASE_URL = 'https://api.bitbucket.org/2.0'

    def __init__(self, username, password, owner='paperclicks'):
        self.username = username
        self.password = password
        self.owner = owner

    def get_repos(self, offset=1, limit=100, query_filter=None):
        """ Get BitBucket repos, the object limit is 100 rows"""

        url = self.BASE_URL + '/repositories/' + self.owner
        query_string = {"pagelen": limit, "page": offset}

        if query_filter is not None:
            query_string.update({"q": query_filter})

        r = requests.get(url, auth=(self.username, self.password), params=query_string)
        result = r.json()

        if r.status_code == 200:
            result = r.json()
            return result

        return result['error']['message']

    def get_repos_by_project(self, project):
        """ Get BitBucket repos filtered by project name, the object limit is 100 rows"""
        repos = self.get_repos(query_filter='project.name="' + project + '"')
        data = {}
        for repo in repos['values']:
            data.update({repo['name']: repo['slug']})

        return repos

    def get_user(self):
        """ Get BitBucket user"""
        url = self.BASE_URL + '/user'
        r = requests.get(url, auth=(self.username, self.password))

        if r.status_code == 200:
            return r.json()

    def get_commits(self, repo, limit=10):
        """ Get BitBucket repo tags, the object limit is 100 rows"""
        url = self.BASE_URL + '/repositories/' + self.owner + '/' + repo + '/commits'
        query_string = {"pagelen": limit}
        result = None

        try:
            r = requests.get(url, auth=(self.username, self.password), params=query_string)
            r.raise_for_status()
            result = r.json()['values']
        except requests.exceptions.HTTPError as e:
            print(e)
            exit(1)

        return result

    def get_last_commit(self, repo):
        """ Get BitBucket repo last commit"""
        return self.get_commits(repo, 1)[0]

    def get_repo_tags(self, repo):
        """ Get BitBucket repo tags, the object limit is 100 rows"""
        url = self.BASE_URL + '/repositories/' + self.owner + '/' + repo + '/refs/tags'
        query_string = {"pagelen": 100}
        r = requests.get(url, auth=(self.username, self.password), params=query_string)
        result = r.json()

        if r.status_code == 200:
            result = r.json()
            return result['values']

        return result['error']['message']

    def get_repo_last_tag(self, repo):
        commit = self.get_last_commit(repo)
        """ Get BitBucket repo tags, the object limit is 100 rows"""
        url = self.BASE_URL + '/repositories/' + self.owner + '/' + repo + '/refs/tags'
        query_string = {
            "pagelen": 100,
            "q": 'target.hash="' + commit['hash'] + '"',
        }
        try:
            r = requests.get(url, auth=(self.username, self.password), params=query_string)
            result = r.json()

            if r.status_code == 200:
                return result['values']

            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            exit(1)

    def self_update(self):
        commit = self.get_last_commit('oly-cli')
        bb_trunc_hash = commit['hash'][0:12]

        link = "https://bitbucket.org/paperclicks/" + Utils.BASE_NAME + "/get/" + bb_trunc_hash + ".zip"
        now = datetime.datetime.now()
        file_name = os.path.join(Utils.OLY_HOME, "oly-" + str(now.isoformat()) + ".zip")
        with open(file_name, "wb") as f:
            try:
                response = requests.get(link, auth=(self.username, self.password), stream=True)
                total_length = response.headers.get('content-length')

                if total_length is not None:
                    dl = 0
                    total_length = int(total_length)
                    with click.progressbar(length=total_length, label='  Downloading', show_eta=False, show_percent=True,
                                           show_pos=False,
                                           bar_template='%(label)s ' + Clr.WARNING + '(%(info)s)' + Clr.RESET) as bar:

                        for data in response.iter_content(chunk_size=100):
                            sleep(0.01)
                            dl += len(data)
                            f.write(data)
                            bar.update(len(data))

                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)
                os.remove(file_name)
                exit(1)

        if zipfile.is_zipfile(file_name):
            with zipfile.ZipFile(file_name) as zf:
                zf.extractall(Utils.OLY_HOME)
            fname = ''
            for folder in glob.glob(os.path.join(Utils.OLY_HOME, '*' + bb_trunc_hash)):
                fname = folder

            if os.path.isdir(Utils.ROOT_DIR):
                shutil.rmtree(Utils.ROOT_DIR)

            os.mkdir(Utils.ROOT_DIR)

            shutil.copytree(fname + '/bin', os.path.join(Utils.ROOT_DIR, 'bin/'))
            shutil.copytree(fname + '/liboly', os.path.join(Utils.ROOT_DIR, 'liboly/'))
            shutil.copyfile(fname + '/oly', os.path.join(Utils.ROOT_DIR, 'oly'))
            os.chmod(os.path.join(Utils.ROOT_DIR, 'oly'), 0o777)
            os.remove(file_name)
            shutil.rmtree(fname)

    @staticmethod
    def clone_service(service, package_name=None):
        if not package_name:
            service_dir = os.path.join(Utils.PROJECTS_DIR, service['slug'])
        else:
            service_dir = os.path.join(Utils.PROJECTS_DIR, package_name, service['slug'])

        if os.path.exists(service_dir):
            print("Service " + Clr.OK + service['slug'] + Clr.RESET + " already exist.")
        else:
            url = ''
            for link in service['links']['clone']:
                if link['name'] == 'ssh':
                    url = link['href']
            subprocess.call("git clone " + url + " " + service_dir, shell=True)
