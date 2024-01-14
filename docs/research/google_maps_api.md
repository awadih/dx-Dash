# Google Maps API

Among the available APIs, The Google Maps Platform APIs offers the Maps Embed API, which is to be used to render map locations.

## The Maps Embed API

With a simple HTTP request and no JavaScript ist required, the map can be embedded using a Maps Embed API URL as **src** for the iframe:

```html 
<iframe
width="600"
height="450"
style="border:0"
loading="lazy"
allowfullscreen
referrerpolicy="no-referrer-when-downgrade"
src="https://www.google.com/maps/embed/v1/place?key=
&q=Space+Needle,Seattle+WA">
</iframe>
```

## Costs

All Maps Embed API requests are available at no charge with unlimited usage.