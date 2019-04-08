import json
import requests
from plantpredict.utilities import convert_json, camel_to_snake, decorate_all_methods
from plantpredict.error_handlers import handle_refused_connection, handle_error_response


@decorate_all_methods(handle_refused_connection)
@decorate_all_methods(handle_error_response)
class Geo(object):
    """
    This API resource does not represent a database entity in PlantPredict. This is a simplified connection to the
    Google Maps API. See Google Maps API Reference for further functionality. (https://developers.google.com/maps/)
    """

    def get_location_info(self):
        """GET /Geo/{Latitude}/{Longitude}/Location

        :return: Example response -
            {
                u'country': u'United States',
                u'country_code': u'US',
                u'locality': u'San Francisco',
                u'region': u'North America',
                u'state_province': u'California',
                u'state_province_code': u'CA'
            }
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/Location".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(json.loads(response.content), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def get_elevation(self):
        """GET /Geo/{Latitude}/{Longitude}/Elevation

        :return: Example response -
            {
                u'elevation': 100.0
            }
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/Elevation".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(json.loads(response.content), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def get_time_zone(self):
        """GET /Geo/{Latitude}/{Longitude}/TimeZone

        :return: Example response -
            {
                u'timeZone': -8.0
            }
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/TimeZone".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(json.loads(response.content), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def __init__(self, api, latitude=None, longitude=None):
        self.api = api

        self.latitude = latitude
        self.longitude = longitude

        super(Geo, self).__init__()
