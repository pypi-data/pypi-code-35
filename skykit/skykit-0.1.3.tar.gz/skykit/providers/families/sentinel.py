import sentinelsat
from sentinelsat import geojson_to_wkt
from skykit.utils.geojson import point_to_geojson, polygon_to_geojson


class Sentinel:
    def __init__(self, username, password, mission, apiURI="https://scihub.copernicus.eu/dhus"):
        if (username == "" or password == ""):
            raise Exception(
                "username and password are mandatory to work with Sentinel dataset")
        self.api = sentinelsat.SentinelAPI(username, password, apiURI)
        self.mission = mission

    def query(self, coordinates, dates, **kwargs):
        geojson = self.__get_geojson(coordinates)
        tiles = self.api.query(geojson_to_wkt(geojson),
                               date=dates,
                               platformname=self.mission,
                               **kwargs)
        return [tiles.get(id) for id in list(tiles)]

    def __get_geojson(self, coordinates):
        if (type(coordinates) == tuple):
            return point_to_geojson(coordinates)
        elif (type(coordinates) == list):
            if (len(coordinates) == 0 or len(coordinates) == 2):
                raise Exception(
                    "Can't build polygon using {} point(s)".format(len(coordinates)))
            elif (len(coordinates) == 1):
                return point_to_geojson(coordinates[0])
            else:
                return polygon_to_geojson(coordinates)
