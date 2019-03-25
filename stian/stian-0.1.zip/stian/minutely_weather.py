import requests
import datetime


class MinutelyWeather:
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

    def minutely_chance_of_rain(self, minute=1):
        """
        Fetches the probability of rain happening as a percentage between 0 and 100 for specified hour in the future.

        Args:
            minute (int): Number of minutes in the future you want to view the forecast for. Upto max 60 minutes.

        Returns:
            float
        """
        try:
            chance_of_rain = (self.weather_report_dict.get("minutely")["data"][minute]["precipProbability"]) * 100
            return chance_of_rain
        except KeyError:
            return "Not Available"

    def minutely_rain_per_hour(self, minute=1):
        """
        Fetches the rainfall in mm per hour for the specified hour in the future.

        Args:
            minute (int): Number of minutes in the future you want to view the forecast for. Upto max 60 minutes.

        Returns:
            float
        """
        try:
            rain_per_hour = self.weather_report_dict.get("minutely")["data"][minute]["precipIntensity"]
            return rain_per_hour
        except KeyError:
            return "Not Available"

    def minutely_time(self, minute=1):
        """
        Fetches the time the current data is valid for in hours, minutes and seconds.

        Args:
            minute (int): Number of minutes in the future you want to view the forecast for. Upto max 60 minutes.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("minutely")["data"][minute]["time"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"
