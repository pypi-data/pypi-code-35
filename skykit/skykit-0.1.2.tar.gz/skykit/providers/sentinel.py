from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from skykit.utils.geojson import point_to_geojson


class Sentinel:
    def __init__(self, username, password, apiURI="https://scihub.copernicus.eu/dhus", source="Sentinel-1"):
        if (username == "" or password == ""):
            raise Exception(
                "username and password are mandatory to work with Sentinel dataset")
        self.api = SentinelAPI(username, password, apiURI)
        self.satellite = source

    def query(self, coordinates, dates, **kwargs):
        geojson = point_to_geojson(coordinates)
        return self.api.query(geojson_to_wkt(geojson),
                              date=dates,
                              platformname=self.satellite,
                              **kwargs)

    def download(self, tiles):
        self.api.download_all(tiles)
