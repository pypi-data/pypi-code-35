import requests
import datetime


class HourlyWeather:
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

    def hourly_summary(self, hour=1):
        """
        Fetches the weather summary for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            string
        """
        try:
            summary = self.weather_report_dict.get("hourly")["data"][hour]["summary"]
            return summary
        except KeyError:
            return "Not Available"

    def hourly_icon(self, hour=1):
        """
        Fetches the weather icon that should be displayed for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            string
        """
        try:
            icon = self.weather_report_dict.get("hourly")["data"][hour]["icon"]
            return icon
        except KeyError:
            return "Not Available"

    def hourly_temperature(self, hour=1):
        """
        Fetches the temperature level in ℃ for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            temperature = self.weather_report_dict.get("hourly")["data"][hour]["temperature"]
            return temperature
        except KeyError:
            return "Not Available"

    def hourly_feels_like(self, hour=1):
        """
        Fetches the feels like temperature in ℃ for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            feels_like = self.weather_report_dict.get("hourly")["data"][hour]["apparentTemperature"]
            return feels_like
        except KeyError:
            return "Not Available"

    def hourly_uv_index(self, hour=1):
        """
        Fetches the uv index level between 1 and 5 for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            int
        """
        try:
            uv_index = self.weather_report_dict.get("hourly")["data"][hour]["uvIndex"]
            return uv_index
        except KeyError:
            return "Not Available"

    def hourly_humidity(self, hour=1):
        """
        Fetches the humidity level and returns a percentage between 0 and 100 for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            humidity = (self.weather_report_dict.get("hourly")["data"][hour]["humidity"]) * 100
            return humidity
        except KeyError:
            return "Not Available"

    def hourly_dew_point(self, hour=1):
        """
        Fetches the dew point level in ℃ for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            dew_point = self.weather_report_dict.get("hourly")["data"][hour]["dewPoint"]
            return dew_point
        except KeyError:
            return "Not Available"

    def hourly_chance_of_rain(self, hour=1):
        """
        Fetches the probability of rain happening as a percentage between 0 and 100 for specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            chance_of_rain = (self.weather_report_dict.get("hourly")["data"][hour]["precipProbability"]) * 100
            return chance_of_rain
        except KeyError:
            return "Not Available"

    def hourly_rain_per_hour(self, hour=1):
        """
        Fetches the rainfall in mm per hour for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            rain_per_hour = self.weather_report_dict.get("hourly")["data"][hour]["precipIntensity"]
            return rain_per_hour
        except KeyError:
            return "Not Available"

    def hourly_visibility(self, hour=1):
        """
        Fetches the visibility level in miles for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            miles
        """
        try:
            visibility = self.weather_report_dict.get("hourly")["data"][hour]["visibility"]
            return visibility
        except KeyError:
            return "Not Available"

    def hourly_cloud_cover(self, hour=1):
        """
        Fetches the cloud cover level as a percentage between 0 and 100 for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            cloud_cover = (self.weather_report_dict.get("hourly")["data"][hour]["cloudCover"]) * 100
            return cloud_cover
        except KeyError:
            return "Not Available"

    def hourly_pressure(self, hour=1):
        """
        Fetches the pressure level in hPa for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            pressure = self.weather_report_dict.get("hourly")["data"][hour]["pressure"]
            return pressure
        except KeyError:
            return "Not Available"

    def hourly_ozone(self, hour=1):
        """
        Fetches the ozone level in dobson units for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            ozone = self.weather_report_dict.get("hourly")["data"][hour]["ozone"]
            return ozone
        except KeyError:
            return "Not Available"

    def hourly_wind_bearing(self, hour=1):
        """
        Fetches the wind bearing degrees with true north at 0 degrees for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            int
        """
        try:
            wind_bearing = self.weather_report_dict.get("hourly")["data"][hour]["windBearing"]
            return wind_bearing
        except KeyError:
            return "Not Available"

    def hourly_wind_speed(self, hour=1):
        """
        Fetches the wind speed level in miles per hour for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            wind_speed = self.weather_report_dict.get("hourly")["data"][hour]["windSpeed"]
            return wind_speed
        except KeyError:
            return "Not Available"

    def hourly_wind_gust(self, hour=1):
        """
        Fetches the wind gust level in miles per hour for the specified hour in the future.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            float
        """
        try:
            wind_gust = self.weather_report_dict.get("hourly")["data"][hour]["windGust"]
            return wind_gust
        except KeyError:
            return "Not Available"

    def hourly_time(self, hour=1):
        """
        Fetches the time the current data is valid for in hours, minutes and seconds.

        Args:
            hour (int): Number of hours in the future you want to view the forecast for. Upto max 48 hours.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("hourly")["data"][hour]["time"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"
