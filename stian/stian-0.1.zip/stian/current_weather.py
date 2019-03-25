import requests
import datetime


class CurrentWeather:
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

        error_data = str(weather_report)
        if error_data == "<Response [403]>":
            raise ValueError("Incorrect Api Key")

        self.weather_report_dict = weather_report.json()

        error_status = self.weather_report_dict.get("error")
        if error_status == "The given location is invalid.":
            raise ValueError("Invalid Latitude / Longitude.")

    def current_summary(self):
        """
        Fetches the current weather summary.

        Returns:
            string
        """
        try:
            summary = self.weather_report_dict.get("currently")["summary"]
            return summary
        except KeyError:
            return "Not Available"

    def current_icon(self):
        """
        Fetches the current weather icon that should be displayed.

        Returns:
            string
        """
        try:
            icon = self.weather_report_dict.get("currently")["icon"]
            return icon
        except KeyError:
            return "Not Available"

    def current_temperature(self):
        """
        Fetches the current temperature level in ℃.

        Returns:
            float
        """
        try:
            temperature = self.weather_report_dict.get("currently")["temperature"]
            return temperature
        except KeyError:
            return "Not Available"

    def current_feels_like(self):
        """
        Fetches the current feels like temperature in ℃.

        Returns:
            float
        """
        try:
            feels_like = self.weather_report_dict.get("currently")["apparentTemperature"]
            return feels_like
        except KeyError:
            return "Not Available"

    def current_uv_index(self):
        """
        Fetches the current uv index level between 1 and 5.

        Returns:
            int
        """
        try:
            uv_index = self.weather_report_dict.get("currently")["uvIndex"]
            return uv_index
        except KeyError:
            return "Not Available"

    def current_humidity(self):
        """
        Fetches the current humidity level and returns a percentage between 0 and 100.

        Returns:
            float
        """
        try:
            humidity = (self.weather_report_dict.get("currently")["humidity"]) * 100
            return humidity
        except KeyError:
            return "Not Available"

    def current_dew_point(self):
        """
        Fetches the current dew point level in ℃.

        Returns:
            float
        """
        try:
            dew_point = self.weather_report_dict.get("currently")["dewPoint"]
            return dew_point
        except KeyError:
            return "Not Available"

    def current_precipitation_type(self):
        """
        Fetches the current precipitation type.

        Returns:
            string
        """
        try:
            precipitation_type = self.weather_report_dict.get("currently")["precipType"]
            return precipitation_type
        except KeyError:
            return "Not Available"

    def current_chance_of_rain(self):
        """
        Fetches the probability of rain happening as a percentage between 0 and 100.

        Returns:
            int
        """
        try:
            chance_of_rain = (self.weather_report_dict.get("currently")["precipProbability"]) * 100
            return chance_of_rain
        except KeyError:
            return "Not Available"

    def current_rain_per_hour_error(self):
        """
        Fetches the current rain per hour error level.

        Returns:
            str
        """
        try:
            rain_per_hour_error = self.weather_report_dict.get("currently")["precipIntensityError"]
            return rain_per_hour_error
        except KeyError:
            return "Not Available"

    def current_rain_per_hour(self):
        """
        Fetches the current rainfall in mm per hour.

        Returns:
            int
        """
        try:
            rain_per_hour = self.weather_report_dict.get("currently")["precipIntensity"]
            return rain_per_hour
        except KeyError:
            return "Not Available"

    def current_visibility(self):
        """
        Fetches the current visibility level in miles.

        Returns:
            miles
        """
        try:
            visibility = self.weather_report_dict.get("currently")["visibility"]
            return visibility
        except KeyError:
            return "Not Available"

    def current_cloud_cover(self):
        """
        Fetches the current cloud cover level as a percentage between 0 and 100.

        Returns:
            float
        """
        try:
            cloud_cover = (self.weather_report_dict.get("currently")["cloudCover"]) * 100
            return cloud_cover
        except KeyError:
            return "Not Available"

    def current_nearest_storm_bearing(self):
        """
        Fetches the current bearing of the nearest storm in degrees.

        Returns:
            int
        """
        try:
            nearest_storm_bearing = self.weather_report_dict.get("currently")["nearestStormBearing"]
            return nearest_storm_bearing
        except KeyError:
            return "Not Available"

    def current_nearest_storm_distance(self):
        """
        Fetches the distance of the nearest storm in miles.

        Returns:
            int
        """
        try:
            nearest_storm_distance = self.weather_report_dict.get("currently")["nearestStormDistance"]
            return nearest_storm_distance
        except KeyError:
            return "Not Available"

    def current_pressure(self):
        """
        Fetches the current pressure level in hPa.

        Returns:
            float
        """
        try:
            pressure = self.weather_report_dict.get("currently")["pressure"]
            return pressure
        except KeyError:
            return "Not Available"

    def current_ozone(self):
        """
        Fetches the current ozone level in dobson units.

        Returns:
            float
        """
        try:
            ozone = self.weather_report_dict.get("currently")["ozone"]
            return ozone
        except KeyError:
            return "Not Available"

    def current_wind_bearing(self):
        """
        Fetches the current wind bearing degrees with true north at 0 degrees.

        Returns:
            int
        """
        try:
            wind_bearing = self.weather_report_dict.get("currently")["windBearing"]
            return wind_bearing
        except KeyError:
            return "Not Available"

    def current_wind_speed(self):
        """
        Fetches the current wind speed level in miles per hour.

        Returns:
            float
        """
        try:
            wind_speed = self.weather_report_dict.get("currently")["windSpeed"]
            return wind_speed
        except KeyError:
            return "Not Available"

    def current_wind_gust(self):
        """
        Fetches the current wind gust level in miles per hour.

        Returns:
            float
        """
        try:
            wind_gust = self.weather_report_dict.get("currently")["windGust"]
            return wind_gust
        except KeyError:
            return "Not Available"

    def current_time(self):
        """
        Fetches the time the current data was last updated in hours, minutes and seconds.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("currently")["time"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"
