# Current user location:

To get such information, two APIs are used:
> [ipapi](https://ipapi.co/): looks for location for specific IP address.<br>
> [ipify](https://www.ipify.org/): a simple public API gives IP address.


```python
import requests
def get_location():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()["ip"]
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
    "ip": ip_address,
    "city": response.get("city"),
    "region": response.get("region"),
    "country": response.get("country_name")
    }
    return location_data
if __name__ == '__main__':
    print(get_location())
```
display:
```json
{
  "ip": "...",
  "city": "Cologne",
  "region": "North Rhine-Westphalia",
  "country": "Germany"
}
```