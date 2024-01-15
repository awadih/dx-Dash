# API free plan limitations

## Sample HTTP request

An example of extensive HTTP request to retrieve the maximum data is given as follow:

```BASH
GET https://api.weatherapi.com/v1/forecast.json?key=API_KEY&q=berlin&alerts=yes&aqi=yes
Content-Type: application/json
```

The response gives for berlin:

1. location: latitude, longitude, timezone, current time, ...etc.
2. weather data for 3 days: weather condition, weather icon for each hour, ... etc.
3. weather alerts if any.

## Free plan features 

The API free of charge plan allows the following:<br />
- HTTPS Protocol<br />
- Realtime weather

## Limitations

The API free of charge still has the following restrictions:<br />
- 1,000,000 calls per month --> around 32,258 per day.<br />
- forcast for up to 3 days

`TODO:`
> Maximize data retrieval per call <br />
> Minimize number of calls in the dash-app

- _Suppose_ a user-per-day target is set to be **100** (each user uses app just once a day), the app should allow a maximum of **320 calls per usage**.<br />
- The actual weather data is updated each **15 Minutes** --> **96 actual-calls per user** are required to maintain reporting live weather data.
`Plan: Use other api to retrieve the current city/town`

## Requirements

This plan requires the usage of a link back, use examples:
As text:
```html
Powered by <a href="https://www.weatherapi.com/" title="Free Weather API">WeatherAPI.com</a>
```
Or as an image:
```html
<a href="https://www.weatherapi.com/" title="Free Weather API"><img src='//cdn.weatherapi.com/v4/images/weatherapi_logo.png' alt="Weather data by WeatherAPI.com" border="0"></a>
```
