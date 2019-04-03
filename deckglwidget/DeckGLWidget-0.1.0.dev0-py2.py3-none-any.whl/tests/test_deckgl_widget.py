#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Andrew Duberstein.
# Distributed under the terms of the Modified BSD License.
import pytest  # noqa

from ..deckgl_widget import DeckGLWidget


def test_example_creation_blank():
    w = DeckGLWidget()
    assert w.json_input == ''
