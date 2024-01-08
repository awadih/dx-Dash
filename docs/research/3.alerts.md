# Alerts

Alerts are retrieved with the Forecast API.

### Syntax

> **Warning:**
> A key 'alerts=yes' should be added to the request.

```http
GET https://api.weatherapi.com/v1/forecast.json?key={{key}}&q=wernigerode&alerts=yes
```

```python
import requests

url = '...'
response = requests.get(url)
# display response as json object (content type mus be application/json)
print(response.json())
# close connection to the server
response.close()
```

```json
{
  "...": "...",
  "alerts": {
    "alert": [
      {
        "headline": "Deutscher Wetterdienst",
        "msgtype": "",
        "severity": "",
        "urgency": "",
        "areas": "",
        "category": "Wind,Wind",
        "certainty": "",
        "event": "gale-force gusts",
        "note": "",
        "effective": "2023-01-12T07:00:00+00:00",
        "expires": "2023-01-12T13:00:00+00:00",
        "desc": "There is a risk of gale-force gusts (Level 2 of 4).\nMax. gusts: ~ 65 km/h; Wind direction: south-west; Increased gusts: near showers and in exposed locations ~ 80 km/h",
        "instruction": ""
      },
      {
        "headline": "Deutscher Wetterdienst",
        "msgtype": "",
        "severity": "",
        "urgency": "",
        "areas": "",
        "category": "",
        "certainty": "",
        "event": "ORKANBÖEN",
        "note": "",
        "effective": "2023-01-11T21:00:00+00:00",
        "expires": "2023-01-12T19:00:00+00:00",
        "desc": "Es treten oberhalb 1000 m Orkanböen mit Geschwindigkeiten um 130 km/h (36 m/s, 70 kn, Bft 12) aus südwestlicher Richtung auf.",
        "instruction": ""
      },
      {
        "headline": "Deutscher Wetterdienst",
        "msgtype": "",
        "severity": "",
        "urgency": "",
        "areas": "",
        "category": "Wind,Wind",
        "certainty": "",
        "event": "hurricane-force gusts",
        "note": "",
        "effective": "2023-01-11T21:00:00+00:00",
        "expires": "2023-01-12T19:00:00+00:00",
        "desc": "There is a risk of hurricane-force gusts (Level 3 of 4).\nHeight range: > 1000 m; Max. gusts: ~ 130 km/h; Wind direction: south-west",
        "instruction": ""
      },
      {
        "headline": "Deutscher Wetterdienst",
        "msgtype": "",
        "severity": "",
        "urgency": "",
        "areas": "",
        "category": "Wind,Wind",
        "certainty": "",
        "event": "gale-force gusts",
        "note": "",
        "effective": "2023-01-12T02:00:00+00:00",
        "expires": "2023-01-13T05:00:00+00:00",
        "desc": "There is a risk of gale-force gusts (Level 2 of 4).\nHeight range: > 600 m; Max. gusts: 65-85 km/h; Wind direction: south-west",
        "instruction": ""
      },
      {
        "headline": "Deutscher Wetterdienst",
        "msgtype": "",
        "severity": "",
        "urgency": "",
        "areas": "",
        "category": "Wind,Wind",
        "certainty": "",
        "event": "wind gusts",
        "note": "",
        "effective": "2023-01-11T23:00:00+00:00",
        "expires": "2023-01-12T07:00:00+00:00",
        "desc": "There is a risk of wind gusts (level 1 of 4).\nMax. gusts: ~ 55 km/h; Wind direction: south-west; Increased gusts: near showers and in exposed locations ~ 65 km/h",
        "instruction": ""
      }
    ]
  }
}
```

### Encoding

- **Strings**: **utf-8** --> simple print will do!

```python
import requests

url = '...'
response = requests.get(url)
json_object = response.json()
# how many alerts are there!?
number_alerts = len(json_object['alerts']['alert'])
# store the fourth alert as json object
alert3 = json_object['alerts']['alert'][3]
# display desc for the alert
print(alert3["desc"])
```
alert3:
```json
{
  "headline": "Deutscher Wetterdienst",
  "msgtype": "",
  "severity": "",
  "urgency": "",
  "areas": "",
  "category": "Wind,Wind",
  "certainty": "",
  "event": "hurricane-force gusts",
  "note": "",
  "effective": "2023-01-12T19:00:00+00:00",
  "expires": "2023-01-13T23:00:00+00:00",
  "desc": "There is a risk of hurricane-force gusts (Level 3 of 4).\nHeight range: > 1000 m; Max. gusts: 100-120 km/h; Wind direction: south-west",
  "instruction": ""
}
```
display:
```
There is a risk of hurricane-force gusts (Level 3 of 4).
Height range: > 1000 m; Max. gusts: 100-120 km/h; Wind direction: south-west
```
Note: the description can be also in other languages.

- **Dates**: ISO 8601 (with time zone as UTC or offset from UTC).
--> To parse the date into a datetime object use the following:
```python
import requests
from dateutil.parser import parse
url = '...'
response = requests.get(url)
json_object = response.json()
alert3 = json_object['alerts']['alert'][3]
time_obj_effective = parse(alert3["effective"])
print(time_obj_effective.strftime('Alert effective starting from the %d, %b %Y at %H:%M o\'clock'))
```
display:
```
Alert effective starting from the 12, Jan 2023 at 07:00 o'clock
```
For datetime.datetime docs check the [link](https://docs.python.org/3/library/datetime.html#datetime.datetime).