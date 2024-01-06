import datetime
import requests

from typing import Any, Dict, List, Union, Callable

from flask import jsonify, request
from geopy.geocoders import Nominatim  # type: ignore
from pytz import timezone
from timezonefinder import TimezoneFinder


def get_days(time: datetime.datetime) -> tuple[str, str]:
    """As the weather API allows retrieving for free only 3 days forecast, gets the next 3 days of weekdays

    Args:
        time: a datetime.datetime for actual time

    Returns:
        tuple giving tomorrow's and after tomorrow's names
    """
    weekday = time.weekday()
    WEEKDAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    if weekday <= 4:
        return WEEKDAYS[weekday + 1], WEEKDAYS[weekday + 2]
    elif weekday == 5:
        return WEEKDAYS[6], WEEKDAYS[0]
    else:
        return WEEKDAYS[0], WEEKDAYS[1]


def get_location(ipgeo_key: str, ip_address: str) -> dict[str, str]:
    """Get the user location using the ip address through the IPGeolocation API

    Args:
        ip_address: string for ip address of user
        ipgeo_key: string for IPGeolocation API key

    Returns:
        dictionary for 'ip' address, 'city' and 'country' of the user
    """
    try:
        response_location = requests.get(
            f'https://api.ipgeolocation.io/ipgeo?apiKey={ipgeo_key}&ip={ip_address}&fields=city,country_name')
        response_location.raise_for_status()
        response = response_location.json()
        location_data = {
            "ip": str(response.get("ip")),
            "city": str(response.get("city")),
            "country": str(response.get("country_name"))
        }
        return location_data
    except requests.exceptions.RequestException as e:
        return {}
    finally:
        pass


def get_weather(weatherapi_key: str, city: str) -> dict[str, Any]:
    """Gets the weatherapi response as json - names 'weather' in the code

    Args:
        weatherapi_key: Weatherapi API Key as string
        city: urban location as string

    Returns:
        Get response as json (Dict of str -> Any)
    """
    # Weatherapi API
    try:
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={weatherapi_key}&q={city}&days=3&alerts=yes&aqi=yes')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {}
    finally:
        pass


def forecast_days(time: datetime.datetime, weather: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Forecast temperatures and retrieve weather icons for 3 days

    Args:
        time: a datetime.datetime for actual time
        weather: full weather data as json (dictionary)

    Returns:
        a dictionary for 'next 3' days, 'weather icon' and 'temperature forecast'
    """
    tomorrow, after_tomorrow = get_days(time)
    return {'TODAY': {'weather_icon': weather['forecast']['forecastday'][0]['day']['condition']['icon'],
                      'temperature': str(weather['forecast']['forecastday'][0]['day']['avgtemp_c']) + '°'},
            tomorrow: {'weather_icon': weather['forecast']['forecastday'][1]['day']['condition']['icon'],
                       'temperature': str(weather['forecast']['forecastday'][1]['day']['avgtemp_c']) + '°'},
            after_tomorrow: {'weather_icon': weather['forecast']['forecastday'][2]['day']['condition']['icon'],
                             'temperature': str(weather['forecast']['forecastday'][2]['day']['avgtemp_c']) + '°'}}


def forecast_params(weather: Dict[str, Any]) -> Dict[str, str]:
    """Give current humidity, pressure and wind speed

    Args:
        weather: full weather data as json (dictionary)

    Returns:
        dictionary for humidity, pressure and wind speed with corresponding units
    """
    humidity = weather["current"]["humidity"]
    pressure = weather["current"]["pressure_mb"]
    wind_speed = weather["current"]["wind_kph"]
    return {'HUMIDITY': f'{humidity}%', 'PRESSURE': f'{pressure} hPa', 'WIND SPEED': f'{wind_speed} kmph'}


def forecast_hours(time: datetime.datetime, weather: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Get the weather forecast for next 24 hours

    Args:
        time: a datetime.datetime for actual time
        weather: full weather data as json (dictionary)

    Returns:
        formatted dictionary with weather forecast as well as corresponding icons
    """
    now = datetime.time(time.hour)
    formatted_weather = {'NOW': {
        'weather_icon': weather['forecast']['forecastday'][0]['hour'][int(now.strftime('%H'))]['condition']['icon'],
        'temperature': str(weather['forecast']['forecastday'][0]['hour'][int(now.strftime('%H'))]['temp_c']),
        'humidity': str(weather['forecast']['forecastday'][0]['hour'][int(now.strftime('%H'))]['humidity']),
        'wind_speed': str(weather['forecast']['forecastday'][0]['hour'][int(now.strftime('%H'))]['wind_kph'])
    }
    }
    i = int(now.strftime('%H')) + 1
    counting = 0
    j = 0
    while i <= 23:
        time = time + datetime.timedelta(hours=1)
        formatted_weather[time.strftime('%I').lstrip('0') + " " + time.strftime('%p').upper()] = {
            'weather_icon': weather['forecast']['forecastday'][j]['hour'][i]['condition']['icon'],
            'temperature': str(weather['forecast']['forecastday'][j]['hour'][i]['temp_c']),
            'humidity': str(weather['forecast']['forecastday'][j]['hour'][i]['humidity']),
            'wind_speed': str(weather['forecast']['forecastday'][j]['hour'][i]['wind_kph'])
        }
        if i + 1 == 24:
            i = 0
            j += 1
        i += 1
        counting += 1
        if counting == 23:
            break
    return formatted_weather


def get_astro(weather: Dict[str, Any]) -> tuple[str, str]:
    """Get sunrise and sunset using weather response

    Args:
        weather: full weather data as json (dictionary)

    Returns:
        tuple with sunrise and sunrise for current location at local time
    """
    return weather["forecast"]["forecastday"][0]["astro"]["sunrise"], weather["forecast"]["forecastday"][0]["astro"][
        "sunset"]


def get_alerts(weather: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Get alerts for location at current time if any

    Args:
        weather: full weather data as json (dictionary)

    Returns:
        tuple with flag if alerts are found and alert headline, event and description
    """
    if weather["alerts"]["alert"]:
        return True, [weather["alerts"]["alert"][0]['headline'], weather["alerts"]["alert"][0]['event'], \
                      weather["alerts"]["alert"][0]['desc']]
    return False, ['', '', '']


def get_src(googleapi_key: str, city: str) -> tuple[str, bool]:
    """Get source link for image or google map using teleport api / Google Maps api

    Args:
        googleapi_key: Google Maps API Key as string
        city: location as string

    Returns:
        a string link to location photo with teleport api, if it's been found, a Google map source link otherwise.
    """
    # TELEPORT API
    try:
        city = city.replace(" ", "-")
        response = requests.get(f'https://api.teleport.org/api/urban_areas/slug:{city}/images/')
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()['photos'][0]['image']['mobile'], True
        else:
            # Google Maps API
            return get_map_link(googleapi_key, city), False
    except Exception as e:
        print(e)
        # Google Maps API
        return get_map_link(googleapi_key, city), False


def get_timezone(city):  # type: ignore
    """Get timezone for given location 'place'

    Args:
        city: string for current location

    Returns:
        timezone for the given location
    """
    geolocator = Nominatim(user_agent="app")
    place_details = geolocator.geocode(city)
    obj = TimezoneFinder()
    time_zone = timezone(obj.timezone_at(lng=place_details[1][1], lat=place_details[1][0]))  # type: ignore
    return time_zone


def get_summary(city: str) -> str:
    """Get a summary about the given city through Teleport API

    Args:
        city: string for given location

    Returns:
        A short summary about the given urban location
    """
    try:
        city = city.replace(" ", "-")
        response = requests.get(f'https://api.teleport.org/api/urban_areas/slug:{city}/scores/')
        response.raise_for_status()
        return response.json()['summary']
    except Exception as e:
        print(e)
        return ''


def get_quality(weather: Dict[str, Any]) -> List[str]:
    """Get actual temperature, how does it feel like, air quality index a corresponding air quality description

    Args:
        weather: full weather data as json (dictionary)

    Returns:
        list with actual temperature, how does it feel like, air quality index a corresponding air quality description
    """
    AIR_Q_DESC = {1: 'Good', 2: 'Moderate', 3: 'Unhealthy for sensitive group', 4: 'Unhealthy', 5: 'Very Unhealthy',
                  6: 'Hazardous'}
    temperature = str(weather["current"]["temp_c"]) + "°"
    feels_like = str(weather["current"]["feelslike_c"]) + "°"
    air_q_index = weather["current"]["air_quality"]["us-epa-index"]
    return [temperature, feels_like, air_q_index, AIR_Q_DESC[air_q_index]]


def get_map_link(googleapi_key, city: str) -> str:
    """Get google map link for city using the Google Maps API Key

    Args:
        googleapi_key: Google Maps api key as string
        city: string for urban location

    Returns:
        source link to embedded map
    """
    return f'https://www.google.com/maps/embed/v1/place?key={googleapi_key}&q={city}&zoom=12'
