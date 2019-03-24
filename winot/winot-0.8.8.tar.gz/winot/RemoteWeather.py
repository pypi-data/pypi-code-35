import urllib
import json

# "https://api.openweathermap.org/data/2.5/weather?q=Bengaluru&appid=1a0622b746356b944847f0e1432e741c&units=metric"

def get_weather_data(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q="
    url = url + city + "&appid="
    with open("wkey.txt", "r") as fh:
        owmkey = fh.read().strip()
    url = url + owmkey
    url = url + "&units=metric"
    try :
        response = urllib.urlopen(url)
        print response.read()
        
        response = json.loads(response.read().strip())
        response = response["main"]
        temp = response["temp"]
        humidity = response["humidity"]
        response = (temp, humidity)
    except Exception as e:
        print "Could not connect to remote weather"
        response = None
    
    return response

class RemoteWeather:
    @staticmethod
    def get_internet_weather(city) :
        return get_weather_data(city)