#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chaostoolkit_openstack` package."""

# import pytest
import os

from chaosopenstack import connect

secrets = {
    "region": os.getenv("OS_REGION_NAME"),
    "auth_url": os.getenv("OS_AUTH_URL"),
    "project_name": os.getenv("OS_TENANT_NAME"),
    "username": os.getenv("OS_USERNAME"),
    "password": os.getenv("OS_PASSWORD"),
}


def test_connect():
    assert connect(secrets=secrets) is not None
