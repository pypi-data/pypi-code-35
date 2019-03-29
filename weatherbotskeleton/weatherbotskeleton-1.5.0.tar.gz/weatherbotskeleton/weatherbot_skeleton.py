import json
import logging
import random
from datetime import datetime, timedelta
from enum import Enum
from os import path

import botskeleton
import pycountry
import requests


HERE = path.abspath(path.dirname(__file__))
WEATHER_ROOT = "http://api.openweathermap.org/data/2.5/weather"

class WeatherbotSkeleton():
    """Class to store things we need for weather."""
    def __init__(
            self,
            *,
            secrets_dir=None,
            owner_url=None,
            version="0.0.0",
            bot_name="A bot",
            delay=0,
            lies=False,
            cities_file=None,

    ):

        if secrets_dir is None:
            raise Exception("Please provide secrets dir!")

        if owner_url is None:
            raise Exception("Please provide owner_url!")

        self.secrets_dir = secrets_dir
        self.owner_url = owner_url
        self.bot_name = bot_name
        self.version = version
        self.place_name = None
        self.json = None
        self.lies = lies
        self.cities_file = cities_file

        user_agent = f"{self.bot_name}/{self.version} ({self.owner_url})"
        self.headers = {"User-Agent": user_agent}

        self.bot_skeleton = botskeleton.BotSkeleton(self.secrets_dir, bot_name=self.bot_name)
        self.bot_skeleton.delay = delay
        self.log = self.bot_skeleton.log

        with open(path.join(self.secrets_dir, "api_key"), "r") as f:
            self.api_key = f.read().strip()


    def produce_status(self, zip_code=None):
        """Produce status from the current weather somewhere."""
        if zip_code is not None:
            self.json, identifier = self.get_weather_from_api(zip_code)
        else:
            self.json, identifier = self.get_weather_from_api()
        self.log.debug(f"Full JSON from weather API: {self.json}")

        # If asked to lie, call for another bit of weather and use that as our name.
        if self.lies:
            name_json, identifier = self.get_weather_from_api()
            self.place_name = identifier
            self.log.info(
                f"Lying, reporting weather from {self.json['name']} under name {self.place_name}")
        else:
            self.place_name = identifier

        thing = random.choice(list(WeatherThings))

        if thing == WeatherThings.WIND_SPEED:
            return self.windspeed_handle()

        elif thing == WeatherThings.CLOUDINESS:
            return self.cloudiness_handle()

        elif thing == WeatherThings.HUMIDITY:
            return self.humidity_handle()

        elif thing == WeatherThings.TEMP:
            return self.temp_handle()

        elif thing == WeatherThings.SUNRISE or thing == WeatherThings.SUNSET:
            return self.sunthing_handle(thing)

    def set_delay(self, delay):
        """Set botskeleton delay. If caller doesn't want to just reach through us to do it."""
        self.bot_skeleton.delay = delay

    def send(self, text):
        """Send through botskeleton. If caller doesn't want to just reach through us to do it."""
        self.bot_skeleton.send(text)

    def nap(self):
        """Nap through botskeleton. If caller doesn't want to just reach through us to do it."""
        self.bot_skeleton.nap()

    # Individual status generators for different kinds of weather stuff.
    def windspeed_handle(self):
        """Handle a status about wind speed."""
        self.log.info("Producing a status on wind speed.")
        wind_speed = float(self.json["wind"]["speed"])

        # Either show in m/s or mph.
        if random.choice([True, False]):
            return random.choice([
                f"The current wind speed in {self.place_name} is {wind_speed} meters/second.",
                f"The wind speed in {self.place_name} is currently {wind_speed} m/s.",
                f"The wind speed in {self.place_name} is {wind_speed} m/s at this moment.",
            ])

        # Close enough?
        imperial_speed = round(wind_speed * 2.237, 2)
        return random.choice([
            f"The current wind speed in {self.place_name} is {imperial_speed} miles per hour.",
            f"The wind speed in {self.place_name} is {imperial_speed} mph.",
            f"The wind speed in {self.place_name} is {imperial_speed} mph last I checked.",
        ])


    def cloudiness_handle(self):
        """Handle a status about clouds."""
        self.log.info("Producing a status on cloudiness.")
        cloudiness = float(self.json["clouds"]["all"])

        # Provide either a status with the exact cloudiness, or one describing roughly how cloudy it
        # is.
        if random.choice([True, False]):
            return random.choice([
                f"The cloudiness in {self.place_name} is {cloudiness}%, currently.",
                f"It is {cloudiness}% cloudy in {self.place_name} right now.",
            ])

        else:
            # Rough encoding of http://forecast.weather.gov/glossary.php?word=sky%20condition.
            # I don't know if OWM's cloudiness percent is supposed to translate to Oktas, but whatever.
            # Clear/Sunny - 0/8 okta.
            if cloudiness < 12.5:
                cloudiness_phrase = random.choice([
                    "It's clear",
                    "There are almost no clouds",
                    "Good luck finding clouds",
                ])

            # Mostly Clear/Mostly Sunny - 1/8 to 2.5/8 okta.
            elif cloudiness >= 12.5 and cloudiness < 31.25:
                cloudiness_phrase = random.choice([
                    "It's not very cloudy",
                    "There are not many clouds",
                    "It's very clear",
                    "It's mostly clear",
                ])

            # Partly Cloudy/Partly Sunny - 2.5/8 to 4.5/8 okta.
            elif cloudiness >= 31.25 and cloudiness < 56.25:
                cloudiness_phrase = random.choice([
                    "It's kinda cloudy",
                    "There are a few clouds",
                    "It's partly clear",
                    "It's partly cloudy",
                ])

            # Mostly Cloudy/Considerable Cloudiness - 4.5/8 to 7.5/8 okta.
            elif cloudiness >= 56.25 and cloudiness < 93.75:
                cloudiness_phrase = random.choice([
                    "It's very cloudy",
                    "It's mostly cloudy",
                    "There are a bunch of clouds",
                    "It's not very clear",
                    "Wow! There are a lot of clouds",
                ])

            # Cloudy - 7.5/8 okta to 8/8 okta.
            else:
                cloudiness_phrase = random.choice([
                    "It's cloudy",
                    "It's not clear",
                    "There are a ton of clouds",
                ])

        return f"{cloudiness_phrase} in {self.place_name}{get_time_descriptor()} " +\
                f"({cloudiness}% cloudiness)."


    def humidity_handle(self):
        """Handle a status about humidity."""
        self.log.info("Producing a status on humidity.")
        humidity = float(self.json["main"]["humidity"])

        # Provide either a status with the exact humidity, or one describing roughly how wet it is.
        if random.choice([True, False]):
            return random.choice([
                f"The humidity in {self.place_name} is {humidity}%, currently.",
                f"It is {humidity}% humid in {self.place_name} right now.",
            ])

        if humidity < 40:
            return random.choice([
                f"It is very dry in {self.place_name} right now ({humidity}% humidity).",
                f"It's very dry in {self.place_name} ({humidity}% humidity).",
            ])

        elif humidity >= 40 and humidity < 75:
            return random.choice([
                f"It's mildly humid in {self.place_name} ({humidity}% humid).",
                f"It's kinda wet in {self.place_name} ({humidity}% humid).",
            ])

        return random.choice([
            f"It's very humid in {self.place_name} ({humidity}% humid).",
            f"It's quite wet in {self.place_name} right now ({humidity}% humid).",
        ])


    def temp_handle(self):
        """Handle a status about the temperature."""
        self.log.info("Producing a status on temperature.")
        temp = self.json["main"]["temp"]

        if random.choice(range(2)) > 0:
            celsius_temp = round(float(temp) - 273.15, 2)
            return f"It's {celsius_temp} °C in {self.place_name} right now."

        fahrenheit_temp = round((float(temp) * (9.0 / 5)) - 459.67, 2)
        return f"It's {fahrenheit_temp} °F in {self.place_name}."


    def sunthing_handle(self, thing):
        """Handle a status about the sunset or sunrise."""
        if thing == WeatherThings.SUNRISE:
            self.log.info("Producing a status on the sunrise.")
            sunthing_time = self.json["sys"]["sunrise"]
            sunthing = "sunrise"

        else:
            self.log.info("Producing a status on the sunset.")
            sunthing_time = self.json["sys"]["sunset"]
            sunthing = "sunset"

        sunthing_datetime = datetime.utcfromtimestamp(int(sunthing_time))
        formatted_datetime = sunthing_datetime.strftime("%H:%M:%S")

        now = datetime.utcnow()

        if abs(now - sunthing_datetime) > timedelta(seconds=60) == sunthing_datetime:
            return random.choice([
                f"The {sunthing} is happening now in {self.place_name}.",
                f"You can watch the {sunthing} now in {self.place_name}.",
                f"You're missing the {sunthing} in {self.place_name}.",
            ])

        if now > sunthing_datetime:
            return random.choice([
                f"The last {sunthing} in {self.place_name} happened at {formatted_datetime} UTC.",
                f"Sorry, you missed the {sunthing} in {self.place_name}, it was at {formatted_datetime}.",
                f"You could have seen the {sunthing} in {self.place_name}. It was at {formatted_datetime}.",
            ])

        return random.choice([
            f"The next {sunthing} in {self.place_name} will happen at {formatted_datetime} UTC.",
            f"You could watch the {sunthing} in {self.place_name} at {formatted_datetime} UTC.",
        ])

    def get_weather_from_api(self, *, zip_code=None, zone="US"):
        """Get weather blob for a random city from the openweathermap API."""
        if zip_code is None:

            if self.cities_file is not None:
                with open(self.cities_file, "r") as f:
                    cities = json.loads(f.read().strip())

                city = random.choice(cities)
                self.log.info(f"Random city is {city}.")

                url = get_city_url(city["id"], self.api_key)

                city_name = city["name"]
                country_code = city["country"]
                country_name = pycountry.countries.get(alpha_2=country_code).name

                identifier = f"{city_name}, {country_name}"

            else:
                zip_code = botskeleton.random_line(path.join(HERE, "ZIP_CODES.txt"))
                self.log.info(f"Random zip code is {zip_code}.")
                url = get_zip_url(zip_code, self.api_key)

                identifier = None

        self.log.info(f"Hitting {url} for weather.")

        weather = openweathermap_api_call(url, self.headers)
        weather_json = weather.json()

        # Handle errors kinda sorta.
        cod = str(weather_json["cod"])
        if cod != "200":
            self.log.info(f"Got non-200 code {cod}.")

            # Handle 404 and 500 with one retry (seems to work for now).
            if cod == "500" or cod == "404":
                self.log.warning(f"Cod is 500 or 404, attempting to retry.")
                weather = openweathermap_api_call(url, self.headers)
                weather_json = weather.json()

            else:
                # TODO expose a bot error handle method in botskeleton,
                # and use that here.
                self.log.error((f"No clue how to handle code {cod} from openweather API. " +
                           f"Full response: {weather_json}"))

        return weather_json, identifier


def get_time_descriptor():
    """Get a phrase like "currently" or "right now", or nothing at all. Provides leading space."""
    return random.choice([" currently", " right now", " this moment", ""])


def get_zip_url(zip_code, api_key):
    """Format a URL to get weather by zip code from the OpenWeatherMap API."""
    return f"{WEATHER_ROOT}?zip={zip_code},us&appid={api_key}"


def get_city_url(city_code, api_key):
    """Format a URL to get weather by city code from the OpenWeatherMap API."""
    return f"{WEATHER_ROOT}?id={city_code}&appid={api_key}"


# Actual rate-limited API calls here.
# Be overly cautious because in my case multiple accounts use this bot skeleton.
@botskeleton.rate_limited(900)
def openweathermap_api_call(url, headers):
    """Perform a rate-limited API call."""
    return requests.get(url, headers=headers)


class WeatherThings(Enum):
    """Kinds of weather we can pull out of a weather blob from the OWM API."""
    WIND_SPEED = 000
    CLOUDINESS = 100
    SUNRISE = 200
    SUNSET = 300
    HUMIDITY = 400
    TEMP = 500
