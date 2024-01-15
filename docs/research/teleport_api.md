# Teleport API

Teleport API offers an outstanding dataset for urban areas. A summary for each city as well as a photo can be accessed with HTTP request.

## Search city

We can find the city names with a simple search, using the following HTTP request:

```BASH 
### City
GET https://api.teleport.org/api/cities/?search=rabat
Content-Type: application/json
```

As a response, we get a JSON with similar city names **rabat**, we notice, that there are cities with similar names among others in Morocco and Malta.

```JSON 
{
"_embedded": {
"city:search-results": [
    {
    "_links": {
        "city:item": {
        "href": "https://api.teleport.org/api/cities/geonameid:2538475/"
        }
    },
    "matching_alternate_names": [
        {"name": "rabat"},
        {"name": "Rabat"},
        {"name": "rabata"},
        {"name": "Rabata"},
        {"name": "Rabatas"},
        {"name": "rabato"},
        {"name": "Rabato"},
        {"name": "Rabatum"}
    ],
    "matching_full_name": "Rabat, Rabat-Salé-Kénitra, Morocco"
    },
    {
    "_links": {
        "city:item": {
        "href": "https://api.teleport.org/api/cities/geonameid:2562620/"
        }
    },
    "matching_alternate_names": [
        {"name": "Rabat"},
        {"name": "Rabatas"},
        {"name": "Rabato"}
    ],
    "matching_full_name": "Rabat, Ir-Rabat, Malta"
    },
    {
    "_links": {
        "city:item": {
        "href": "https://api.teleport.org/api/cities/geonameid:3044669/"
        }
    },
    "matching_alternate_names": [
        {"name": "Rabatotfalu"}
    ],
    "matching_full_name": "Szentgotthárd, Vas, Hungary (Rabatotfalu)"
    },
    {
    "_links": {
        "city:item": {
        "href": "https://api.teleport.org/api/cities/geonameid:2562619/"
        }
    },
    "matching_alternate_names": [
        {"name": "Rabat"}
    ],
    "matching_full_name": "Victoria, Victoria, Malta (Rabat)"
    },
    {
    "_links": {
        "city:item": {
        "href": "https://api.teleport.org/api/cities/geonameid:1128310/"
        }
    },
    "matching_alternate_names": [
        {"name": "Rabat-e Sangi"},
        {"name": "Rabat-e Sangi-ye Pa'in"},
        {"name": "Rabat-i-Sangi-Pa'in"},
        {"name": "Rabati-Sangiyi-Pain"}
    ],
    "matching_full_name": "Rabāţ-e Sangī-ye Pā’īn, Herat, Afghanistan (Rabat-e Sangi)"
    }
    ]
    },
    ...
```

## Photo of city

Besides, the API offers a photo for cities. The access goes here also per HTTP request:

```BASH 
### Photo for city
GET https://api.teleport.org/api/urban_areas/slug:paris/images/
```

As a Json response the API gives the following:

```JSON
...
"photos": [
    {
    "attribution": {
    "license": "Attribution, ShareAlike",
    "photographer": "Rob Potvin",
    "site": "Unsplash",
    "source": "https://unsplash.com/robpotvin"
    },
    "image": {
    "mobile": "https://d13k13wj6adfdf.cloudfront.net/urban_areas/paris-0ae0bb626e.jpg",
    "web": "https://d13k13wj6adfdf.cloudfront.net/urban_areas/paris_web-0a3c7314a5.jpg"
      }
]
```

A link to the photo can be then retrieved:
[Paris](https://d13k13wj6adfdf.cloudfront.net/urban_areas/paris_web-0a3c7314a5.jpg).

## Summary for city

A summary for each urban area can be retrieved with HTTP request:

```BASH
### search timezone
GET https://api.teleport.org/api/urban_areas/slug:cologne/scores/
```

A response sees like the following:
```JSON
...
    "score_out_of_10": 5.289000000000001
    }
  ],
    "summary": "<p>Cologne, Germany, is among the top cities with a <b>free business environment</b>.\n\n    \n        According to our city rankings, this is a good place to live with high ratings in <b>travel connectivity</b>, <b>safety</b> and <b>healthcare</b>.\n    \n\n    \n</p>\n\n",
    "teleport_city_score": 62.26432432432431
}
```

The summary can be added to HTML as follows, where *summary* is the variable holding the summary:

```HTML
<p class="lead m-1">{{ summary | safe }}</p>
```

## Costs

Teleport API is available at no charge with unlimited usage.