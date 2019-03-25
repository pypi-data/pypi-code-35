import requests


class MiscWeather:
    """Fetches weather data and allows querying individual values."""

    def __init__(self):
        """Constructor for weather class."""
        self.weather_report_dict = {}

    def update(self, api_key, latitude, longitude):
        """
        Fetches an updated dictionary for the weather class.

        Args:
            api_key (string): Api key provided form darksky.net website.
            latitude (float): Latitude to update weather data on.
            longitude (float): Longitude to update weather data on.

        Returns:
            None
        """
        try:
            weather_report = requests.get(
                "https://api.darksky.net/forecast/" + api_key + "/" + str(latitude) + "," + str(longitude) +
                "?units=uk2")
        except requests.ConnectionError:
            return "Connection Error"
        self.weather_report_dict = weather_report.json()

    def misc_latitude(self):
        """
        Fetches the latitude used for the current forecast.

        Returns:
            float
        """
        try:
            latitude = (self.weather_report_dict.get("latitude"))
            return latitude
        except KeyError:
            return "Not Available"

    def misc_longitude(self):
        """
        Fetches the longitude used for the current forecast.

        Returns:
            float
        """
        try:
            longitude = (self.weather_report_dict.get("longitude"))
            return longitude
        except KeyError:
            return "Not Available"

    def misc_units(self):
        """
        Fetches the units used for the current forecast.

        Returns:
            string
        """
        try:
            units = (self.weather_report_dict.get("flags")["units"])
            return units
        except KeyError:
            return "Not Available"

    def misc_sources(self):
        """
        Fetches the sources used for the current forecast.

        Returns:
            list
        """
        try:
            sources = (self.weather_report_dict.get("flags")["sources"])
            return sources
        except KeyError:
            return "Not Available"

    def misc_nearest_station(self):
        """
        Fetches the distance to the nearest weather station used for the current forecast in miles.

        Returns:
            float
        """
        try:
            nearest_station = (self.weather_report_dict.get("flags")["nearest-station"])
            return nearest_station
        except KeyError:
            return "Not Available"

    def misc_meteoalarm_license(self):
        """
        Fetches the meteoalarm license.

        Returns:
            string
        """
        try:
            meteo_license = (self.weather_report_dict.get("flags")["meteoalarm-license"])
            return meteo_license
        except KeyError:
            return "Not Available"

    def misc_timezone(self):
        """
        Fetches the timezone used for the current forecast.

        Returns:
            string
        """
        try:
            timezone = (self.weather_report_dict.get("timezone"))
            return timezone
        except KeyError:
            return "Not Available"
