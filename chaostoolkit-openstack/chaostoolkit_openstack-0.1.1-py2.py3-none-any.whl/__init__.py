# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.discovery.discover import (
    discover_actions,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.exceptions import DiscoveryFailed
from chaoslib.types import (
    Configuration,
    Discovery,
    DiscoveredActivities,
    DiscoveredSystemInfo,
    Secrets,
)

import openstack

__version__ = '0.1.1'
__all__ = ["__version__", "discover", "connect"]


def connect(
    configuration: Configuration = None, secrets: Secrets = None
) -> openstack.connection.Connection:
    return openstack.connect(
        auth_url=secrets["auth_url"],
        project_name=secrets["project_name"],
        username=secrets["username"],
        password=secrets["password"],
        region_name=secrets["region"],
    )


def discover(discover_system: bool = True) -> Discovery:
    logger.info("Discovering capabilities from chaostoolkit-openstack")

    discovery = initialize_discovery_result(
        "chaostoolkit-openstack", __version__, "openstack"
    )
    discovery["activities"].extend(load_exported_activities())
    return discovery


def load_exported_activities() -> List[DiscoveredActivities]:
    activities = []
    activities.extend(discover_actions("chaosopenstack.compute.actions"))
    activities.extend(discover_probes("chaosopenstack.compute.probes"))
    return activities
