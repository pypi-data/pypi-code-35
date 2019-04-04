#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chaostoolkit_openstack` package."""

# import pytest
import os

from chaosopenstack.compute.probes import check_server_name

secrets = {
    "region": os.getenv("OS_REGION_NAME"),
    "auth_url": os.getenv("OS_AUTH_URL"),
    "project_name": os.getenv("OS_TENANT_NAME"),
    "username": os.getenv("OS_USERNAME"),
    "password": os.getenv("OS_PASSWORD"),
}


def test_server_name():
    assert check_server_name(name="foo", secrets=secrets) == 0
