# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import os
import shutil
import easyauth

project_skeleton_files = [
    "test/settings",
    "test/__init__.py",
    "test/apps.py",
    "test/wsgi.py",
    "manage.py",
    "requirements.txt",
    ".gitignore"
]


gui_files = [
    "vue-ui/build",
    "vue-ui/config",
    "vue-ui/src",
    "vue-ui/static",
    "vue-ui/.babelrc",
    "vue-ui/.editorconfig",
    "vue-ui/.gitignore",
    "vue-ui/.postcssrc.js",
    "vue-ui/index.html",
    "vue-ui/package.json",
    "vue-ui/package-lock.json",
    "vue-ui/README.md"
]


project_skeleton_dir_name = "project_skeleton"


def __copy_files(src_files, dest, src_prefix=""):
    for f in src_files:
        abs_f = os.path.join(src_prefix, f)
        if os.path.isdir(abs_f):
            shutil.copytree(abs_f, os.path.join(dest, f))
        else:
            shutil.copy(abs_f, os.path.join(dest, f))


def __add_easy_auth_dep(req_deps_file):
    with open(req_deps_file, "a") as req_file:
        req_file.write("\n{}".format("easyauth"))


def __create_user_mode(dir):
    user_mode_code = '''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from easyauth.models import AbstractUser  
    

class User(AbstractUser):
    pass  
'''
    with open(os.path.join(dir, "models.py"), "w") as req_file:
        req_file.write("{}\n".format(user_mode_code))


def __create_urls(dir):
    urls = '''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from easyauth import urls as auth_urls
from easyauth import admin_urls as user_admin_urls

router = routers.DefaultRouter(trailing_slash=False)

# app apis: register apis for your own app
# router.register(r'api/view_path', view_class, base_name='view_name')

urlpatterns = router.urls
urlpatterns += [
    # url(r'^admin/', admin.site.urls),
    # auth apis including login, password reset
    url(r'^api-auth/', include(auth_urls)),
    # user crud apis - only used by administrator
    url(r'^api/', include(user_admin_urls)),
] 
'''
    with open(os.path.join(dir, "urls.py"), "w") as req_file:
        req_file.write("{}\n".format(urls))


def prepare_project_skeleton_for_setup():
    clean_prepared_project_skeleton_after_setup()
    os.makedirs(project_skeleton_dir_name)
    __copy_files(project_skeleton_files, project_skeleton_dir_name)
    __create_user_mode(os.path.join(os.path.join(project_skeleton_dir_name, "test")))
    __create_urls(os.path.join(os.path.join(project_skeleton_dir_name, "test")))
    __add_easy_auth_dep(os.path.join(project_skeleton_dir_name, "requirements.txt"))
    __copy_files(gui_files, project_skeleton_dir_name)


def get_data_files_for_setup():
    all_data_files = []
    for root, dirs, files in os.walk(project_skeleton_dir_name):
        all_data_files.append((root, [os.path.join(root, f) for f in files]))
    return all_data_files


def get_package_data_for_setup(dir):
    all_package_data = []
    base_folder_name = os.path.basename(dir)
    parent_folder_name = dir[:-len(base_folder_name)]
    for root, dirs, files in os.walk(dir):
        all_package_data += [os.path.join(root[len(parent_folder_name):], f) for f in files]
    return all_package_data


def clean_prepared_project_skeleton_after_setup():
    if os.path.exists(project_skeleton_dir_name):
        shutil.rmtree(project_skeleton_dir_name)


def generate_project(project_name):
    cwd = os.getcwd()
    project_path = os.path.join(cwd, project_name)
    if os.path.exists(project_path):
        print("project %s already existed, remove it first..." % project_path)
        shutil.rmtree(project_path)
    print("generate project {} located {}...".format(project_name, project_path))
    project_skeleton_dir = os.path.join(os.path.dirname(os.path.dirname(easyauth.__file__)), project_skeleton_dir_name)
    os.makedirs(project_path)
    __copy_files(os.listdir(project_skeleton_dir), project_path, project_skeleton_dir)
    os.rename(os.path.join(project_path, "test"), os.path.join(project_path, project_name))


def parse_args():
    parser = argparse.ArgumentParser\
        (description="Automatically generate a project including easyauth app based on Django and rest framework")
    parser.add_argument("project_name", help="specify the project name.")
    return parser.parse_args()


def main():
    args = parse_args()
    generate_project(args.project_name)
