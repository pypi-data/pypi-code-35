#!/usr/bin/env python3

from enum import Enum, unique
from itertools import chain


class CsvData:
    samples = 'samples'
    timestamp = 'timestamp'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'


class DataTypeId:
    clusters = 'clusters'
    metropme = 'metropme'
    roads = 'roads'
    tomtomfcd = 'tomtomfcd'
    zones = 'zones'


class AttId:
    att = 'att'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    length = 'length'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    tono = 'tono'
    webatt = 'webatt'

    datapointeid = 'datapointeid'
    roadeid = 'roadeid'
    validfrom = 'validfrom'
    validto = 'validto'
    zoneeid = 'zoneeid'


class NetworkObjId:
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    newdatapoints = 'newdatapoints'
    omiteddatapoints = 'omiteddatapoints'
    roadsffspeedmap = 'roadsffspeedmap'
