#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
from concurrent.futures import ProcessPoolExecutor
import json
import io

from gv_services.proto.common_pb2 import TrafficData
from gv_services.proto.geographer_pb2 import Locations, Mapping
from gv_utils import csv, enums, geometry


ATT = enums.AttId.att
DATATYPE_EID = enums.AttId.datatypeeid
EID = enums.AttId.eid
GEOM = enums.AttId.geom
WEBATT = enums.AttId.webatt


async def encode_traffic_data(trafficdata):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        pbtrafficdata = await loop.run_in_executor(pool, _csv_dumps_bytes, trafficdata)
    return TrafficData(data=pbtrafficdata)


def _csv_dumps_bytes(data):
    return csv.dumps(data).getvalue()


async def decode_traffic_data(response):
    pbtrafficdata = response.data
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, _csv_loads_bytes, pbtrafficdata)
    return data


def _csv_loads_bytes(pbtrafficdata):
    return csv.loads(io.BytesIO(pbtrafficdata))


async def encode_locations(locations):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        pblocations = await loop.run_in_executor(pool, _encode_locations, locations)
    return pblocations


def _encode_locations(locations, pblocations=None):
    if pblocations is None:
        pblocations = Locations()
    for eid, loc in locations.items():
        pblocations.locations[eid].geom = loc[GEOM].wkb
        pblocations.locations[eid].att.FromJsonString(json.dumps(loc.get(ATT, {})))
        pblocations.locations[eid].webatt.FromJsonString(json.dumps(loc.get(WEBATT, {})))
        pblocations.locations[eid].datatype = loc.get(DATATYPE_EID, '')
    return pblocations


async def decode_locations(response):
    loop = asyncio.get_event_loop()
    locations = await loop.run_in_executor(None, _decode_locations, response.locations)
    return locations


def _decode_locations(pblocations):
    locations = {}
    for eid in pblocations:
        loc = pblocations[eid]
        locations[eid] = {EID: eid, GEOM: geometry.decode_geometry(loc.geom),
                          ATT: json.loads(loc.att.ToJsonString()), WEBATT: json.loads(loc.webatt.ToJsonString()),
                          DATATYPE_EID: loc.datatype}
    return locations


async def encode_mapping(mapping, validat):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        pbmapping = await loop.run_in_executor(pool, _encode_mapping, mapping, validat)
    return pbmapping


def _encode_mapping(mapping, validat):
    pbmapping = Mapping()
    for fromeid, toeidsorlocations in mapping.items():
        if not isinstance(toeidsorlocations, dict):
            pbmapping.mapping[fromeid].eids.eids.extend(toeidsorlocations)
        else:
            _encode_locations(toeidsorlocations, pbmapping.mapping[fromeid].locations)
    pbmapping.validat.FromSeconds(validat)
    return pbmapping


async def decode_mapping(response):
    loop = asyncio.get_event_loop()
    mapping = await loop.run_in_executor(None, _decode_mapping, response.mapping)
    return mapping, response.validat.ToSeconds()


def _decode_mapping(pbmapping):
    mapping = {}
    for eid in pbmapping:
        if pbmapping[eid].HasField('eids'):
            mapping[eid] = pbmapping[eid].eids.eids
        else:
            mapping[eid] = _decode_locations(pbmapping[eid].locations.locations)
    return mapping
