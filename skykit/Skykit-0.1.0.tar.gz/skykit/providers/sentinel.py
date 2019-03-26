from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from skykit.utils.geojson import point_to_geojson


class Sentinel:
    def __init__(self, username, password, apiURI="https://scihub.copernicus.eu/dhus"):
        if (username == "" or password == ""):
            raise Exception(
                "username and password are mandatory to work with Sentinel dataset")
        self.api = SentinelAPI(username, password, apiURI)
        self.tiles = []

    def get_tiles(self, source, coordinates, dates, **kwargs):
        geojson = point_to_geojson(coordinates)
        self.tiles = self.api.query(geojson_to_wkt(geojson),
                                    date=dates,
                                    platformname=source,
                                    **kwargs)
        return self.tiles

    def download(self):
        self.api.download_all(self.tiles)
