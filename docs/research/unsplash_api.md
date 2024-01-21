# Teleport API

Unsplash API offers an outstanding dataset of images. A random photo in the urban area can be accessed with HTTP request.

## Search image with city name

We can find an imgae in the city with the city name using the following HTTP request:

```BASH 
### Photo in city
GET https://api.unsplash.com/search/photos?client_id=API_KEY&query=CITY_NAME
Content-Type: application/json
```

As a result:

```JSON
"total": 523,
"total_pages": 53,
"results": [
    {
    "id": "18fvXEV1R_A",
    "slug": "brown-concrete-building-under-blue-sky-during-daytime-18fvXEV1R_A",
    "created_at": "2020-02-11T18:08:27Z",
    "updated_at": "2024-01-21T05:14:18Z",
    "promoted_at": null,
    "width": 3968,
    "height": 2976,
    "color": "#d9d9f3",
    "blur_hash": "LkMtR7t6krof%%j[jsofI9a|nhjY",
    "description": " Hassan II Mosque in Casablanca, Morocco",
    "alt_description": "brown concrete building under blue sky during daytime",
    "breadcrumbs": [],
    "urls": {
        "raw": "https://images.unsplash.com/photo-1581443459255-e895f2a4222f?ixid=M3w1NTQ4Mjl8MHwxfHNlYXJjaHwxfHxjYXNhYmxhbmNhfGVufDB8fHx8MTcwNTgzNTM4Nnww&ixlib=rb-4.0.3",
        "full": "https://images.unsplash.com/photo-1581443459255-e895f2a4222f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w1NTQ4Mjl8MHwxfHNlYXJjaHwxfHxjYXNhYmxhbmNhfGVufDB8fHx8MTcwNTgzNTM4Nnww&ixlib=rb-4.0.3&q=85",
        "regular": "https://images.unsplash.com/photo-1581443459255-e895f2a4222f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NTQ4Mjl8MHwxfHNlYXJjaHwxfHxjYXNhYmxhbmNhfGVufDB8fHx8MTcwNTgzNTM4Nnww&ixlib=rb-4.0.3&q=80&w=1080",
        "small": "https://images.unsplash.com/photo-1581443459255-e895f2a4222f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NTQ4Mjl8MHwxfHNlYXJjaHwxfHxjYXNhYmxhbmNhfGVufDB8fHx8MTcwNTgzNTM4Nnww&ixlib=rb-4.0.3&q=80&w=400",
        "thumb": "https://images.unsplash.com/photo-1581443459255-e895f2a4222f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NTQ4Mjl8MHwxfHNlYXJjaHwxfHxjYXNhYmxhbmNhfGVufDB8fHx8MTcwNTgzNTM4Nnww&ixlib=rb-4.0.3&q=80&w=200",
        "small_s3": "https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1581443459255-e895f2a4222f"
        },
...
```

## Costs

Unsplash API is available at no charge with unlimited usage.