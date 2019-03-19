# -*- coding: utf-8 -*-
from endi.default_layouts import DefaultLayout


def includeme(config):
    """
    Include the layout in the current configuration

    :param obj config: A Configurator object
    """
    config.add_layout(
        DefaultLayout,
        "endi:templates/layouts/login.mako"
    )
    config.add_layout(
        DefaultLayout,
        "endi:templates/layouts/login.mako",
        name='login'
    )
