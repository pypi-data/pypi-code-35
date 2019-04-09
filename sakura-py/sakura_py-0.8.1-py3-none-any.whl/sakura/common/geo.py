import json

class GeoPoint:
    def __init__(self, lng, lat):
        self.geojson = json.dumps(
            dict(
                type = 'Point',
                coordinates = [ lng, lat ]
            ))

class GeoRegion:
    def __init__(self, geojson):
        self.geojson = geojson
        self.SQL_OP = 'IN'
    def __contains__(self, col):
        return col.__in__(self)

class GeoPolygon(GeoRegion):
    def __init__(self, lnglat):
        geojson = json.dumps(
            dict(
                type = 'Polygon',
                coordinates = [[ lnglat ]]
            ))
        GeoRegion.__init__(self, geojson)

class GeoRectangle(GeoPolygon):
    def __init__(self, lngwest, lngeast, latsouth, latnorth):
        lnglat = (
            (lngwest, latnorth),
            (lngeast, latnorth),
            (lngeast, latsouth),
            (lngwest, latsouth),
            (lngwest, latnorth)
        )
        GeoPolygon.__init__(self, lnglat)

