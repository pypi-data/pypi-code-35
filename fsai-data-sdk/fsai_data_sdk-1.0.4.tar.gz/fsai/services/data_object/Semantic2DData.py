# Generated classes by https://app.quicktype.io/
# Replace "@" by "attributes" in json file
# Then generate the python class.
# Then replace "u@attributes" by "u@"
# Rename the parser semantic2_d_data_from_dict and semantic2_d_
# data_to_dict function into semantic_2d_data_from_dict and semantic_2d_data_to_dict

# GENERATED CODE
# coding: utf-8

#
# To use this code in Python 2.7 you'll have to
#
#     pip install enum34

# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = semantic2d_data_from_dict(json.loads(json_string))

from datetime import datetime
from uuid import UUID
from enum import Enum
import dateutil.parser


def from_int(x):
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x):
    assert isinstance(x, (str, unicode))
    return x


def from_datetime(x):
    return dateutil.parser.parse(x)


def from_float(x):
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x):
    assert isinstance(x, float)
    return x


def to_class(c, x):
    assert isinstance(x, c)
    return x.to_dict()


def from_none(x):
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f, x):
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x):
    assert isinstance(x, bool)
    return x


def to_enum(c, x):
    assert isinstance(x, c)
    return x.value


class HeaderAttributes:
    def __init__(self, rev_major, rev_minor, name, version, date, north, south, east, west, vendor):
        self.rev_major = rev_major
        self.rev_minor = rev_minor
        self.name = name
        self.version = version
        self.date = date
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.vendor = vendor

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        rev_major = from_int(obj.get(u"revMajor"))
        rev_minor = from_int(obj.get(u"revMinor"))
        name = from_str(obj.get(u"name"))
        version = from_str(obj.get(u"version"))
        date = from_datetime(obj.get(u"date"))
        north = from_float(obj.get(u"north"))
        south = from_float(obj.get(u"south"))
        east = from_float(obj.get(u"east"))
        west = from_float(obj.get(u"west"))
        vendor = from_str(obj.get(u"vendor"))
        return HeaderAttributes(rev_major, rev_minor, name, version, date, north, south, east, west, vendor)

    def to_dict(self):
        result = {}
        result[u"revMajor"] = from_int(self.rev_major)
        result[u"revMinor"] = from_int(self.rev_minor)
        result[u"name"] = from_str(self.name)
        result[u"version"] = from_str(self.version)
        result[u"date"] = self.date.isoformat()
        result[u"north"] = to_float(self.north)
        result[u"south"] = to_float(self.south)
        result[u"east"] = to_float(self.east)
        result[u"west"] = to_float(self.west)
        result[u"vendor"] = from_str(self.vendor)
        return result


class Header:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = HeaderAttributes.from_dict(obj.get(u"@"))
        return Header(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(HeaderAttributes, self.attributes)
        return result


class JunctionAttributes:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        id = UUID(obj.get(u"id"))
        return JunctionAttributes(id)

    def to_dict(self):
        result = {}
        result[u"id"] = str(self.id)
        return result


class ConnectionAttributes:
    def __init__(self, id, incoming_road, connecting_road, contact_point):
        self.id = id
        self.incoming_road = incoming_road
        self.connecting_road = connecting_road
        self.contact_point = contact_point

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        id = UUID(obj.get(u"id"))
        incoming_road = UUID(obj.get(u"incomingRoad"))
        connecting_road = UUID(obj.get(u"connectingRoad"))
        contact_point = from_str(obj.get(u"contactPoint"))
        return ConnectionAttributes(id, incoming_road, connecting_road, contact_point)

    def to_dict(self):
        result = {}
        result[u"id"] = str(self.id)
        result[u"incomingRoad"] = str(self.incoming_road)
        result[u"connectingRoad"] = str(self.connecting_road)
        result[u"contactPoint"] = from_str(self.contact_point)
        return result


class LaneLinkAttributes:
    def __init__(self, attributes_from, to):
        self.attributes_from = attributes_from
        self.to = to

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes_from = from_union([from_none, lambda x: UUID(x)], obj.get(u"from"))
        to = from_union([from_none, lambda x: UUID(x)], obj.get(u"to"))
        return LaneLinkAttributes(attributes_from, to)

    def to_dict(self):
        result = {}
        result[u"from"] = from_union([from_none, lambda x: str(x)], self.attributes_from)
        result[u"to"] = from_union([from_none, lambda x: str(x)], self.to)
        return result


class LaneLink:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = LaneLinkAttributes.from_dict(obj.get(u"@"))
        return LaneLink(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(LaneLinkAttributes, self.attributes)
        return result


class ObjectOverlapGroup:
    def __init__(self, object_reference):
        self.object_reference = object_reference

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        object_reference = from_list(lambda x: x, obj.get(u"objectReference"))
        return ObjectOverlapGroup(object_reference)

    def to_dict(self):
        result = {}
        result[u"objectReference"] = from_list(lambda x: x, self.object_reference)
        return result


class Connection:
    def __init__(self, attributes, lane_link, object_overlap_group):
        self.attributes = attributes
        self.lane_link = lane_link
        self.object_overlap_group = object_overlap_group

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = ConnectionAttributes.from_dict(obj.get(u"@"))
        lane_link = from_list(LaneLink.from_dict, obj.get(u"laneLink"))
        object_overlap_group = ObjectOverlapGroup.from_dict(obj.get(u"objectOverlapGroup"))
        return Connection(attributes, lane_link, object_overlap_group)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(ConnectionAttributes, self.attributes)
        result[u"laneLink"] = from_list(lambda x: to_class(LaneLink, x), self.lane_link)
        result[u"objectOverlapGroup"] = to_class(ObjectOverlapGroup, self.object_overlap_group)
        return result


class CornerGlobalAttributes:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        x = from_union([from_float, from_none], obj.get(u"x"))
        y = from_union([from_float, from_none], obj.get(u"y"))
        z = from_int(obj.get(u"z"))
        return CornerGlobalAttributes(x, y, z)

    def to_dict(self):
        result = {}
        result[u"x"] = from_union([to_float, from_none], self.x)
        result[u"y"] = from_union([to_float, from_none], self.y)
        result[u"z"] = from_int(self.z)
        return result


class CornerGlobal:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = CornerGlobalAttributes.from_dict(obj.get(u"@"))
        return CornerGlobal(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(CornerGlobalAttributes, self.attributes)
        return result


class Outline:
    def __init__(self, corner_global):
        self.corner_global = corner_global

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        corner_global = from_list(CornerGlobal.from_dict, obj.get(u"cornerGlobal"))
        return Outline(corner_global)

    def to_dict(self):
        result = {}
        result[u"cornerGlobal"] = from_list(lambda x: to_class(CornerGlobal, x), self.corner_global)
        return result


class Junction:
    def __init__(self, attributes, outline, connection):
        self.attributes = attributes
        self.outline = outline
        self.connection = connection

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = JunctionAttributes.from_dict(obj.get(u"@"))
        outline = Outline.from_dict(obj.get(u"outline"))
        connection = from_list(Connection.from_dict, obj.get(u"connection"))
        return Junction(attributes, outline, connection)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(JunctionAttributes, self.attributes)
        result[u"outline"] = to_class(Outline, self.outline)
        result[u"connection"] = from_list(lambda x: to_class(Connection, x), self.connection)
        return result


class RoadAttributes:
    def __init__(self, name, length, id, junction):
        self.name = name
        self.length = length
        self.id = id
        self.junction = junction

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        name = from_str(obj.get(u"name"))
        length = from_float(obj.get(u"length"))
        id = UUID(obj.get(u"id"))
        junction = UUID(obj.get(u"junction"))
        return RoadAttributes(name, length, id, junction)

    def to_dict(self):
        result = {}
        result[u"name"] = from_str(self.name)
        result[u"length"] = to_float(self.length)
        result[u"id"] = str(self.id)
        result[u"junction"] = str(self.junction)
        return result


class ElevationProfile:
    def __init__(self, ):
        pass

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        return ElevationProfile()

    def to_dict(self):
        result = {}
        return result


class LanesAttributes:
    def __init__(self, single_side):
        self.single_side = single_side

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        single_side = from_bool(obj.get(u"singleSide"))
        return LanesAttributes(single_side)

    def to_dict(self):
        result = {}
        result[u"singleSide"] = from_bool(self.single_side)
        return result


class LaneSectionAttributes:
    def __init__(self, s):
        self.s = s

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        s = from_int(obj.get(u"s"))
        return LaneSectionAttributes(s)

    def to_dict(self):
        result = {}
        result[u"s"] = from_int(self.s)
        return result


class PurpleType(Enum):
    LEFTBOUNDARY = u"LEFTBOUNDARY"
    RIGHTBOUNDARY = u"RIGHTBOUNDARY"


class BoundaryAttributes:
    def __init__(self, type):
        self.type = type

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        type = PurpleType(obj.get(u"type"))
        return BoundaryAttributes(type)

    def to_dict(self):
        result = {}
        result[u"type"] = to_enum(PurpleType, self.type)
        return result


class PointSet:
    def __init__(self, point):
        self.point = point

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        point = from_list(CornerGlobal.from_dict, obj.get(u"point"))
        return PointSet(point)

    def to_dict(self):
        result = {}
        result[u"point"] = from_list(lambda x: to_class(CornerGlobal, x), self.point)
        return result


class BoundaryGeometry:
    def __init__(self, point_set):
        self.point_set = point_set

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        point_set = PointSet.from_dict(obj.get(u"pointSet"))
        return BoundaryGeometry(point_set)

    def to_dict(self):
        result = {}
        result[u"pointSet"] = to_class(PointSet, self.point_set)
        return result


class Boundary:
    def __init__(self, attributes, geometry):
        self.attributes = attributes
        self.geometry = geometry

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = BoundaryAttributes.from_dict(obj.get(u"@"))
        geometry = BoundaryGeometry.from_dict(obj.get(u"geometry"))
        return Boundary(attributes, geometry)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(BoundaryAttributes, self.attributes)
        result[u"geometry"] = to_class(BoundaryGeometry, self.geometry)
        return result


class Boundaries:
    def __init__(self, boundary):
        self.boundary = boundary

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        boundary = from_list(Boundary.from_dict, obj.get(u"boundary"))
        return Boundaries(boundary)

    def to_dict(self):
        result = {}
        result[u"boundary"] = from_list(lambda x: to_class(Boundary, x), self.boundary)
        return result


class Direction(Enum):
    FORWARD = u"FORWARD"


class TurnType(Enum):
    NOTURN = u"NOTURN"


class FluffyType(Enum):
    BIKING = u"BIKING"
    DRIVING = u"DRIVING"
    NONE = u"NONE"


class LaneAttributes:
    def __init__(self, id, uid, type, direction, turn_type):
        self.id = id
        self.uid = uid
        self.type = type
        self.direction = direction
        self.turn_type = turn_type

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        id = from_int(obj.get(u"id"))
        uid = UUID(obj.get(u"uid"))
        type = FluffyType(obj.get(u"type"))
        direction = Direction(obj.get(u"direction"))
        turn_type = TurnType(obj.get(u"turnType"))
        return LaneAttributes(id, uid, type, direction, turn_type)

    def to_dict(self):
        result = {}
        result[u"id"] = from_int(self.id)
        result[u"uid"] = str(self.uid)
        result[u"type"] = to_enum(FluffyType, self.type)
        result[u"direction"] = to_enum(Direction, self.direction)
        result[u"turnType"] = to_enum(TurnType, self.turn_type)
        return result


class BorderTypesAttributes:
    def __init__(self, s_offset, e_offset):
        self.s_offset = s_offset
        self.e_offset = e_offset

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        s_offset = from_int(obj.get(u"sOffset"))
        e_offset = from_int(obj.get(u"eOffset"))
        return BorderTypesAttributes(s_offset, e_offset)

    def to_dict(self):
        result = {}
        result[u"sOffset"] = from_int(self.s_offset)
        result[u"eOffset"] = from_int(self.e_offset)
        return result


class Color(Enum):
    NONE = u"NONE"
    WHITE = u"WHITE"
    YELLOW = u"YELLOW"


class TentacledType(Enum):
    BROKEN = u"BROKEN"
    NONE = u"NONE"
    SOLID = u"SOLID"


class BorderTypeAttributes:
    def __init__(self, type, color):
        self.type = type
        self.color = color

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        type = from_union([from_none, TentacledType], obj.get(u"type"))
        color = from_union([from_none, Color], obj.get(u"color"))
        return BorderTypeAttributes(type, color)

    def to_dict(self):
        result = {}
        result[u"type"] = from_union([from_none, lambda x: to_enum(TentacledType, x)], self.type)
        result[u"color"] = from_union([from_none, lambda x: to_enum(Color, x)], self.color)
        return result


class BorderType:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = BorderTypeAttributes.from_dict(obj.get(u"@"))
        return BorderType(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(BorderTypeAttributes, self.attributes)
        return result


class BorderTypes:
    def __init__(self, attributes, border_type):
        self.attributes = attributes
        self.border_type = border_type

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = BorderTypesAttributes.from_dict(obj.get(u"@"))
        border_type = from_list(BorderType.from_dict, obj.get(u"borderType"))
        return BorderTypes(attributes, border_type)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(BorderTypesAttributes, self.attributes)
        result[u"borderType"] = from_list(lambda x: to_class(BorderType, x), self.border_type)
        return result


class Border:
    def __init__(self, geometry, border_types):
        self.geometry = geometry
        self.border_types = border_types

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        geometry = BoundaryGeometry.from_dict(obj.get(u"geometry"))
        border_types = BorderTypes.from_dict(obj.get(u"borderTypes"))
        return Border(geometry, border_types)

    def to_dict(self):
        result = {}
        result[u"geometry"] = to_class(BoundaryGeometry, self.geometry)
        result[u"borderTypes"] = to_class(BorderTypes, self.border_types)
        return result


class RoadLink:
    def __init__(self, predecessor, successor, neighbor):
        self.predecessor = predecessor
        self.successor = successor
        self.neighbor = neighbor

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        predecessor = ElevationProfile.from_dict(obj.get(u"predecessor"))
        successor = ElevationProfile.from_dict(obj.get(u"successor"))
        neighbor = ElevationProfile.from_dict(obj.get(u"neighbor"))
        return RoadLink(predecessor, successor, neighbor)

    def to_dict(self):
        result = {}
        result[u"predecessor"] = to_class(ElevationProfile, self.predecessor)
        result[u"successor"] = to_class(ElevationProfile, self.successor)
        result[u"neighbor"] = to_class(ElevationProfile, self.neighbor)
        return result


class SpeedAttributes:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        min = from_int(obj.get(u"min"))
        max = from_int(obj.get(u"max"))
        return SpeedAttributes(min, max)

    def to_dict(self):
        result = {}
        result[u"min"] = from_int(self.min)
        result[u"max"] = from_int(self.max)
        return result


class Speed:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = SpeedAttributes.from_dict(obj.get(u"@"))
        return Speed(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(SpeedAttributes, self.attributes)
        return result


class PurpleLane:
    def __init__(self, attributes, link, center_line, border, speed, signal_overlap_group, object_overlap_group, sample_associations, junction_overlap_group, lane_overlap_group):
        self.attributes = attributes
        self.link = link
        self.center_line = center_line
        self.border = border
        self.speed = speed
        self.signal_overlap_group = signal_overlap_group
        self.object_overlap_group = object_overlap_group
        self.sample_associations = sample_associations
        self.junction_overlap_group = junction_overlap_group
        self.lane_overlap_group = lane_overlap_group

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = LaneAttributes.from_dict(obj.get(u"@"))
        link = RoadLink.from_dict(obj.get(u"link"))
        center_line = ElevationProfile.from_dict(obj.get(u"centerLine"))
        border = Border.from_dict(obj.get(u"border"))
        speed = Speed.from_dict(obj.get(u"speed"))
        signal_overlap_group = ElevationProfile.from_dict(obj.get(u"signalOverlapGroup"))
        object_overlap_group = ElevationProfile.from_dict(obj.get(u"objectOverlapGroup"))
        sample_associations = ElevationProfile.from_dict(obj.get(u"sampleAssociations"))
        junction_overlap_group = ElevationProfile.from_dict(obj.get(u"junctionOverlapGroup"))
        lane_overlap_group = ElevationProfile.from_dict(obj.get(u"laneOverlapGroup"))
        return PurpleLane(attributes, link, center_line, border, speed, signal_overlap_group, object_overlap_group, sample_associations, junction_overlap_group, lane_overlap_group)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(LaneAttributes, self.attributes)
        result[u"link"] = to_class(RoadLink, self.link)
        result[u"centerLine"] = to_class(ElevationProfile, self.center_line)
        result[u"border"] = to_class(Border, self.border)
        result[u"speed"] = to_class(Speed, self.speed)
        result[u"signalOverlapGroup"] = to_class(ElevationProfile, self.signal_overlap_group)
        result[u"objectOverlapGroup"] = to_class(ElevationProfile, self.object_overlap_group)
        result[u"sampleAssociations"] = to_class(ElevationProfile, self.sample_associations)
        result[u"junctionOverlapGroup"] = to_class(ElevationProfile, self.junction_overlap_group)
        result[u"laneOverlapGroup"] = to_class(ElevationProfile, self.lane_overlap_group)
        return result


class CenterLane:
    def __init__(self, lane):
        self.lane = lane

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        lane = from_list(PurpleLane.from_dict, obj.get(u"lane"))
        return CenterLane(lane)

    def to_dict(self):
        result = {}
        result[u"lane"] = from_list(lambda x: to_class(PurpleLane, x), self.lane)
        return result


class Center:
    def __init__(self, lane):
        self.lane = lane

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        lane = CenterLane.from_dict(obj.get(u"lane"))
        return Center(lane)

    def to_dict(self):
        result = {}
        result[u"lane"] = to_class(CenterLane, self.lane)
        return result


class Cessor:
    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = from_union([JunctionAttributes.from_dict, from_none], obj.get(u"@"))
        return Cessor(attributes)

    def to_dict(self):
        result = {}
        result[u"@"] = from_union([lambda x: to_class(JunctionAttributes, x), from_none], self.attributes)
        return result


class PurpleLink:
    def __init__(self, predecessor, successor, neighbor):
        self.predecessor = predecessor
        self.successor = successor
        self.neighbor = neighbor

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        predecessor = Cessor.from_dict(obj.get(u"predecessor"))
        successor = Cessor.from_dict(obj.get(u"successor"))
        neighbor = ElevationProfile.from_dict(obj.get(u"neighbor"))
        return PurpleLink(predecessor, successor, neighbor)

    def to_dict(self):
        result = {}
        result[u"predecessor"] = to_class(Cessor, self.predecessor)
        result[u"successor"] = to_class(Cessor, self.successor)
        result[u"neighbor"] = to_class(ElevationProfile, self.neighbor)
        return result


class FluffyLane:
    def __init__(self, attributes, link, center_line, border, speed, signal_overlap_group, object_overlap_group, sample_associations, junction_overlap_group, lane_overlap_group):
        self.attributes = attributes
        self.link = link
        self.center_line = center_line
        self.border = border
        self.speed = speed
        self.signal_overlap_group = signal_overlap_group
        self.object_overlap_group = object_overlap_group
        self.sample_associations = sample_associations
        self.junction_overlap_group = junction_overlap_group
        self.lane_overlap_group = lane_overlap_group

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = LaneAttributes.from_dict(obj.get(u"@"))
        link = PurpleLink.from_dict(obj.get(u"link"))
        center_line = ElevationProfile.from_dict(obj.get(u"centerLine"))
        border = Border.from_dict(obj.get(u"border"))
        speed = Speed.from_dict(obj.get(u"speed"))
        signal_overlap_group = ElevationProfile.from_dict(obj.get(u"signalOverlapGroup"))
        object_overlap_group = ElevationProfile.from_dict(obj.get(u"objectOverlapGroup"))
        sample_associations = ElevationProfile.from_dict(obj.get(u"sampleAssociations"))
        junction_overlap_group = ElevationProfile.from_dict(obj.get(u"junctionOverlapGroup"))
        lane_overlap_group = ElevationProfile.from_dict(obj.get(u"laneOverlapGroup"))
        return FluffyLane(attributes, link, center_line, border, speed, signal_overlap_group, object_overlap_group, sample_associations, junction_overlap_group, lane_overlap_group)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(LaneAttributes, self.attributes)
        result[u"link"] = to_class(PurpleLink, self.link)
        result[u"centerLine"] = to_class(ElevationProfile, self.center_line)
        result[u"border"] = to_class(Border, self.border)
        result[u"speed"] = to_class(Speed, self.speed)
        result[u"signalOverlapGroup"] = to_class(ElevationProfile, self.signal_overlap_group)
        result[u"objectOverlapGroup"] = to_class(ElevationProfile, self.object_overlap_group)
        result[u"sampleAssociations"] = to_class(ElevationProfile, self.sample_associations)
        result[u"junctionOverlapGroup"] = to_class(ElevationProfile, self.junction_overlap_group)
        result[u"laneOverlapGroup"] = to_class(ElevationProfile, self.lane_overlap_group)
        return result


class LeftLane:
    def __init__(self, lane):
        self.lane = lane

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        lane = from_list(FluffyLane.from_dict, obj.get(u"lane"))
        return LeftLane(lane)

    def to_dict(self):
        result = {}
        result[u"lane"] = from_list(lambda x: to_class(FluffyLane, x), self.lane)
        return result


class Left:
    def __init__(self, lane):
        self.lane = lane

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        lane = LeftLane.from_dict(obj.get(u"lane"))
        return Left(lane)

    def to_dict(self):
        result = {}
        result[u"lane"] = to_class(LeftLane, self.lane)
        return result


class LaneSection:
    def __init__(self, attributes, boundaries, left, right, center):
        self.attributes = attributes
        self.boundaries = boundaries
        self.left = left
        self.right = right
        self.center = center

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = LaneSectionAttributes.from_dict(obj.get(u"@"))
        boundaries = Boundaries.from_dict(obj.get(u"boundaries"))
        left = Left.from_dict(obj.get(u"left"))
        right = Left.from_dict(obj.get(u"right"))
        center = Center.from_dict(obj.get(u"center"))
        return LaneSection(attributes, boundaries, left, right, center)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(LaneSectionAttributes, self.attributes)
        result[u"boundaries"] = to_class(Boundaries, self.boundaries)
        result[u"left"] = to_class(Left, self.left)
        result[u"right"] = to_class(Left, self.right)
        result[u"center"] = to_class(Center, self.center)
        return result


class Lanes:
    def __init__(self, attributes, lane_section):
        self.attributes = attributes
        self.lane_section = lane_section

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = LanesAttributes.from_dict(obj.get(u"@"))
        lane_section = from_list(LaneSection.from_dict, obj.get(u"laneSection"))
        return Lanes(attributes, lane_section)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(LanesAttributes, self.attributes)
        result[u"laneSection"] = from_list(lambda x: to_class(LaneSection, x), self.lane_section)
        return result


class StickyType(Enum):
    ARROW = u"ARROW"
    CONSTRUCTIONCONES = u"CONSTRUCTIONCONES"
    CROSSWALK = u"CROSSWALK"
    ROADMARK = u"ROADMARK"


class ObjectAttributes:
    def __init__(self, type, id):
        self.type = type
        self.id = id

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        type = StickyType(obj.get(u"type"))
        id = UUID(obj.get(u"id"))
        return ObjectAttributes(type, id)

    def to_dict(self):
        result = {}
        result[u"type"] = to_enum(StickyType, self.type)
        result[u"id"] = str(self.id)
        return result


class Object:
    def __init__(self, attributes, outline):
        self.attributes = attributes
        self.outline = outline

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = ObjectAttributes.from_dict(obj.get(u"@"))
        outline = Outline.from_dict(obj.get(u"outline"))
        return Object(attributes, outline)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(ObjectAttributes, self.attributes)
        result[u"outline"] = to_class(Outline, self.outline)
        return result


class Objects:
    def __init__(self, object):
        self.object = object

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        object = from_list(Object.from_dict, obj.get(u"object"))
        return Objects(object)

    def to_dict(self):
        result = {}
        result[u"object"] = from_list(lambda x: to_class(Object, x), self.object)
        return result


class GeometryAttributes:
    def __init__(self, s_offset, x, y, z, length):
        self.s_offset = s_offset
        self.x = x
        self.y = y
        self.z = z
        self.length = length

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        s_offset = from_int(obj.get(u"sOffset"))
        x = from_float(obj.get(u"x"))
        y = from_float(obj.get(u"y"))
        z = from_int(obj.get(u"z"))
        length = from_float(obj.get(u"length"))
        return GeometryAttributes(s_offset, x, y, z, length)

    def to_dict(self):
        result = {}
        result[u"sOffset"] = from_int(self.s_offset)
        result[u"x"] = to_float(self.x)
        result[u"y"] = to_float(self.y)
        result[u"z"] = from_int(self.z)
        result[u"length"] = to_float(self.length)
        return result


class GeometryElement:
    def __init__(self, attributes, point_set):
        self.attributes = attributes
        self.point_set = point_set

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        attributes = GeometryAttributes.from_dict(obj.get(u"@"))
        point_set = PointSet.from_dict(obj.get(u"pointSet"))
        return GeometryElement(attributes, point_set)

    def to_dict(self):
        result = {}
        result[u"@"] = to_class(GeometryAttributes, self.attributes)
        result[u"pointSet"] = to_class(PointSet, self.point_set)
        return result


class RouteView:
    def __init__(self, geometry):
        self.geometry = geometry

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        geometry = from_list(GeometryElement.from_dict, obj.get(u"geometry"))
        return RouteView(geometry)

    def to_dict(self):
        result = {}
        result[u"geometry"] = from_list(lambda x: to_class(GeometryElement, x), self.geometry)
        return result


class Signals:
    def __init__(self, signal):
        self.signal = signal

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        signal = from_list(lambda x: x, obj.get(u"signal"))
        return Signals(signal)

    def to_dict(self):
        result = {}
        result[u"signal"] = from_list(lambda x: x, self.signal)
        return result


class Road:
    def __init__(self, link, route_view, elevation_profile, lateral_profile, lanes, objects, signals, attributes):
        self.link = link
        self.route_view = route_view
        self.elevation_profile = elevation_profile
        self.lateral_profile = lateral_profile
        self.lanes = lanes
        self.objects = objects
        self.signals = signals
        self.attributes = attributes

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        link = RoadLink.from_dict(obj.get(u"link"))
        route_view = RouteView.from_dict(obj.get(u"routeView"))
        elevation_profile = ElevationProfile.from_dict(obj.get(u"elevationProfile"))
        lateral_profile = ElevationProfile.from_dict(obj.get(u"lateralProfile"))
        lanes = Lanes.from_dict(obj.get(u"lanes"))
        objects = Objects.from_dict(obj.get(u"objects"))
        signals = Signals.from_dict(obj.get(u"signals"))
        attributes = RoadAttributes.from_dict(obj.get(u"@"))
        return Road(link, route_view, elevation_profile, lateral_profile, lanes, objects, signals, attributes)

    def to_dict(self):
        result = {}
        result[u"link"] = to_class(RoadLink, self.link)
        result[u"routeView"] = to_class(RouteView, self.route_view)
        result[u"elevationProfile"] = to_class(ElevationProfile, self.elevation_profile)
        result[u"lateralProfile"] = to_class(ElevationProfile, self.lateral_profile)
        result[u"lanes"] = to_class(Lanes, self.lanes)
        result[u"objects"] = to_class(Objects, self.objects)
        result[u"signals"] = to_class(Signals, self.signals)
        result[u"@"] = to_class(RoadAttributes, self.attributes)
        return result


class Semantic2DData:
    def __init__(self, header, road, junction):
        self.header = header
        self.road = road
        self.junction = junction

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get(u"header"))
        road = from_list(Road.from_dict, obj.get(u"road"))
        junction = from_list(Junction.from_dict, obj.get(u"junction"))
        return Semantic2DData(header, road, junction)

    def to_dict(self):
        result = {}
        result[u"header"] = to_class(Header, self.header)
        result[u"road"] = from_list(lambda x: to_class(Road, x), self.road)
        result[u"junction"] = from_list(lambda x: to_class(Junction, x), self.junction)
        return result


def semantic_2d_data_from_dict(s):
    return Semantic2DData.from_dict(s)


def semantic_2d_data_to_dict(x):
    return to_class(Semantic2DData, x)
