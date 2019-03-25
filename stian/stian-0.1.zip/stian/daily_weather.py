import requests
import datetime


class DailyWeather:
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

    def daily_summary(self, day=1):
        """
        Fetches the weather summary for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            summary = self.weather_report_dict.get("daily")["data"][day]["summary"]
            return summary
        except KeyError:
            return "Not Available"

    def daily_summary_week(self):
        """
        Fetches the weather summary for the week ahead.

        Returns:
            string
        """
        try:
            summary = self.weather_report_dict.get("daily")["summary"]
            return summary
        except KeyError:
            return "Not Available"

    def daily_icon(self, day=1):
        """
        Fetches the weather icon that should be displayed for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            icon = self.weather_report_dict.get("daily")["data"][day]["icon"]
            return icon
        except KeyError:
            return "Not Available"

    def daily_temperature_min(self, day=1):
        """
        Fetches the minimum temperature for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            temperature_min = self.weather_report_dict.get("daily")["data"][day]["temperatureMin"]
            return temperature_min
        except KeyError:
            return "Not Available"

    def daily_temperature_min_time(self, day=1):
        """
        Fetches the time when the temperature is at it's minimum for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["temperatureMinTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_feels_like_min(self, day=1):
        """
        Fetches the minimum feels like temperature for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            feels_like_max = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureMin"]
            return feels_like_max
        except KeyError:
            return "Not Available"

    def daily_feels_like_min_time(self, day=1):
        """
        Fetches the time when the feels like temperature is at it's min for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureMinTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_temperature_max(self, day=1):
        """
        Fetches the maximum temperature for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            temperature_max = self.weather_report_dict.get("daily")["data"][day]["temperatureMax"]
            return temperature_max
        except KeyError:
            return "Not Available"

    def daily_temperature_max_time(self, day=1):
        """
        Fetches the time when the temperature is at it's max for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["temperatureMaxTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_feels_like_max(self, day=1):
        """
        Fetches the maximum feels like temperature for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            feels_like_max = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureMax"]
            return feels_like_max
        except KeyError:
            return "Not Available"

    def daily_feels_like_max_time(self, day=1):
        """
        Fetches the time when the feels like temperature is at it's max for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureMaxTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_temperature_low(self, day=1):
        """
        Fetches the lowest temperature during the night for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            temperature_low = self.weather_report_dict.get("daily")["data"][day]["temperatureLow"]
            return temperature_low
        except KeyError:
            return "Not Available"

    def daily_temperature_low_time(self, day=1):
        """
        Fetches the time when the temperature is at it's lowest during the night on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["temperatureLowTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_feels_like_low(self, day=1):
        """
        Fetches the feels like temperature lowest point during night for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            ozone = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureLow"]
            return ozone
        except KeyError:
            return "Not Available"

    def daily_feels_like_low_time(self, day=1):
        """
        Fetches the time when the feels like temperature is at it's lowest during the night on the specified day
        in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureLowTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_temperature_high(self, day=1):
        """
        Fetches the day time high temperature for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            uv_index = self.weather_report_dict.get("daily")["data"][day]["temperatureHigh"]
            return uv_index
        except KeyError:
            return "Not Available"

    def daily_temperature_high_time(self, day=1):
        """
        Fetches the time when temperature is at it's highest during the day on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["temperatureHighTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_feels_like_high(self, day=1):
        """
        Fetches the daily feels like temperature high during daytime for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            ozone = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureHigh"]
            return ozone
        except KeyError:
            return "Not Available"

    def daily_feels_like_high_time(self, day=1):
        """
        Fetches the time when the feels like temperature is at it's high for the day on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["apparentTemperatureHighTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_sunrise_time(self, day=1):
        """
        Fetches the time when the sunrises on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["sunriseTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_sunset_time(self, day=1):
        """
        Fetches the time the sunsets for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["sunsetTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_uv_index(self, day=1):
        """
        Fetches the uv index level between 1 and 5 for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            int
        """
        try:
            uv_index = self.weather_report_dict.get("daily")["data"][day]["uvIndex"]
            return uv_index
        except KeyError:
            return "Not Available"

    def daily_uv_index_time(self, day=1):
        """
        Fetches the time when the uv index is highest on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["uvIndexTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_humidity(self, day=1):
        """
        Fetches the humidity level and returns a percentage between 0 and 100 for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            humidity = (self.weather_report_dict.get("daily")["data"][day]["humidity"]) * 100
            return humidity
        except KeyError:
            return "Not Available"

    def daily_dew_point(self, day=1):
        """
        Fetches the dew point level in ℃ for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            dew_point = self.weather_report_dict.get("daily")["data"][day]["dewPoint"]
            return dew_point
        except KeyError:
            return "Not Available"

    def daily_precipitation_type(self, day=1):
        """
        Fetches the current precipitation type.

        Returns:
            string
        """
        try:
            precipitation_type = self.weather_report_dict.get("daily")["data"][day]["precipType"]
            return precipitation_type
        except KeyError:
            return "Not Available"

    def daily_chance_of_rain(self, day=1):
        """
        Fetches the probability of rain happening as a percentage between 0 and 100 for specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            chance_of_rain = (self.weather_report_dict.get("daily")["data"][day]["precipProbability"]) * 100
            return chance_of_rain
        except KeyError:
            return "Not Available"

    def daily_rain_per_hour(self, day=1):
        """
        Fetches the rainfall in mm per hour for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            rain_per_day = self.weather_report_dict.get("daily")["data"][day]["precipIntensity"]
            return rain_per_day
        except KeyError:
            return "Not Available"

    def daily_rain_per_hour_max_time(self, day=1):
        """
        Fetches the time when rainfall is at it's highest on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["precipIntensityMaxTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_visibility(self, day=1):
        """
        Fetches the visibility level in miles for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            miles
        """
        try:
            visibility = self.weather_report_dict.get("daily")["data"][day]["visibility"]
            return visibility
        except KeyError:
            return "Not Available"

    def daily_cloud_cover(self, day=1):
        """
        Fetches the cloud cover level as a percentage between 0 and 100 for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            cloud_cover = (self.weather_report_dict.get("daily")["data"][day]["cloudCover"]) * 100
            return cloud_cover
        except KeyError:
            return "Not Available"

    def daily_pressure(self, day=1):
        """
        Fetches the pressure level in hPa for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            pressure = self.weather_report_dict.get("daily")["data"][day]["pressure"]
            return pressure
        except KeyError:
            return "Not Available"

    def daily_ozone(self, day=1):
        """
        Fetches the ozone level in dobson units for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            ozone = self.weather_report_dict.get("daily")["data"][day]["ozone"]
            return ozone
        except KeyError:
            return "Not Available"

    def daily_wind_bearing(self, day=1):
        """
        Fetches the wind bearing degrees with true north at 0 degrees for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            int
        """
        try:
            wind_bearing = self.weather_report_dict.get("daily")["data"][day]["windBearing"]
            return wind_bearing
        except KeyError:
            return "Not Available"

    def daily_wind_speed(self, day=1):
        """
        Fetches the wind speed level in miles per day for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            wind_speed = self.weather_report_dict.get("daily")["data"][day]["windSpeed"]
            return wind_speed
        except KeyError:
            return "Not Available"

    def daily_wind_gust(self, day=1):
        """
        Fetches the wind gust level in miles per day for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            wind_gust = self.weather_report_dict.get("daily")["data"][day]["windGust"]
            return wind_gust
        except KeyError:
            return "Not Available"

    def daily_wind_gust_time(self, day=1):
        """
        Fetches the time when wind gust speed is at its highest on the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["windGustTime"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%H:%M:%S')
            return time_string
        except KeyError:
            return "Not Available"

    def daily_moon_phase(self, day=1):
        """
        Fetches the fractional part of the lunation number for the specified day in the future.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            float
        """
        try:
            moon_phase = self.weather_report_dict.get("daily")["data"][day]["moonPhase"]
            return moon_phase
        except KeyError:
            return "Not Available"

    def daily_time(self, day=1):
        """
        Fetches the time the current data is valid for in days, minutes and seconds.

        Args:
            day (int): Number of days in the future you want to view the forecast for. Upto max 7 days.

        Returns:
            string
        """
        try:
            time_epoch = self.weather_report_dict.get("daily")["data"][day]["time"]
            time_string = datetime.datetime.fromtimestamp(time_epoch).strftime('%A')
            return time_string
        except KeyError:
            return "Not Available"
