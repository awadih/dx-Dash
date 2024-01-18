from datetime import datetime
from pprint import pprint
from pydantic import BaseModel, field_validator


class Condition(BaseModel):
    text: str
    icon: str

    @classmethod
    @field_validator('icon')
    def icon_must_be_valid(cls, value: str) -> str:
        response = requests.get('https:' + value)
        if response.status_code != 200:
            raise ValueError('icon url invalid!')
        return value


class ForecastDay(BaseModel):
    avgtemp_c: float
    avghumidity: float
    condition: Condition


class Astro(BaseModel):
    sunrise: str
    sunset: str


class ForecastHour(BaseModel):
    time: datetime
    temp_c: float
    condition: Condition
    wind_kph: float
    pressure_mb: float
    humidity: float
    feelslike_c: float


class Alerts(BaseModel):
    headline: str
    event: str
    desc: str


if __name__ == '__main__':
    import requests

    resp = requests.get(
        'https://api.weatherapi.com/v1/forecast.json?key=bea853d469e0444dbe7152331220507&q=new-york&days=3&alerts=yes'
        '&aqi=yes')

    # For each day of the 3 days forecast
    forecast_hour = list()
    for i in range(3):
        forecastDay = ForecastDay(**resp.json()['forecast']['forecastday'][i]['day'])
        astro = Astro(**resp.json()['forecast']['forecastday'][i]['astro'])
        # For each hour of the day, starting from 0 A.M.
        for j in range(24):
            forecastHour = ForecastHour(**resp.json()['forecast']['forecastday'][i]['hour'][j])
            forecast_hour.append(forecastHour)
    pprint(forecast_hour)

    # Many alerts:
    for a in range(len(resp.json()['alerts']['alert'])):
        alerts = Alerts(**resp.json()['alerts']['alert'][a])
        pprint(alerts.desc.replace("\n", "").replace("*", "\n*"))
