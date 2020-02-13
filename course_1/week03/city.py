import pprint
import requests
from dateutil.parser import parser

print(isinstance(list, list))

class OpenWeatherForecast:

    def get(self, city):
        url = "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22"
        data = requests.get(url).json()
        forecast = []
        forecast.append({
            "date": data["dt"],
            "temp": data["main"]["temp"]
        })
        return forecast

class CityInfo:

    def __init__(self, city, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or OpenWeatherForecast()

    def weather_forecast(self):
       self._weather_forecast.get(self.city)

def _main():
    city_info = CityInfo("Moscow")
    forecast = city_info.weather_forecast()
    pprint.pprint(forecast)

if __name__ == "__main__":
    _main()