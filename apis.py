import requests
import os
import json

query = {
    'appid': os.environ['OPEN_WEATHER_KEY'],
    'lat': '52.52',
    'lon': '13.40',
    'exclude': 'minutely,hourly'
}

oneCallUrl = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={appid}&exclude={exclude}&units=metric'

def getOpenWeatherOneCall():
    try:
        r = requests.get(oneCallUrl.format_map(query))
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

if __name__ == "__main__":
    data = getOpenWeatherOneCall()
    print(json.dumps(data, indent=4))
