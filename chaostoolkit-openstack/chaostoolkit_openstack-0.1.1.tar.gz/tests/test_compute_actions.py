#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chaostoolkit_openstack` package."""

# import pytest
import os
import time

from chaosopenstack.compute.actions import start_server, stop_server

secrets = {
    "region": os.getenv("OS_REGION_NAME"),
    "auth_url": os.getenv("OS_AUTH_URL"),
    "project_name": os.getenv("OS_TENANT_NAME"),
    "username": os.getenv("OS_USERNAME"),
    "password": os.getenv("OS_PASSWORD"),
}


def test_server_start_stop():
    assert stop_server(server_name="cas01-ddt01-dev", secrets=secrets) == 1
    time.sleep(30)
    assert start_server(server_name="cas01-ddt01-dev", secrets=secrets) == 1
