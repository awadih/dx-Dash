# Development plan

Here is a list of all todos required to build the app.

`TODO: App-Performance`
> It's recommended to use the python package [orjson](https://github.com/ijl/orjson) for Data Serialization instead of json. See [details](https://dash.plotly.com/performance).
```shell
pip install --upgrade orjson
```
> Use **WebGL** to render graphs.<br />
Example:<br />
```python
import pandas as pd
import numpy as np
import plotly.express as px
N = 1000
df = pd.DataFrame(dict(x=np.random.randn(N), y=np.random.randn(N)))
fig = px.scatter(df, x="x", y="y", render_mode='webgl')
```

`TODO: App-Flexibility`
> Maximize data retrieval per call <br />
> Minimize number of calls in the dash-app

`TODO: current location`
> Current location through IP address see [page](research/1.current_location.md).

`Requirements:`
> Update for dash components each 15 minutes, as the actual weather data is updated each 15 Minutes. <br />
- Use dcc.Interval for live updates:<br />
The dcc.Interval element allows you to update components on a predefined interval. The n_intervals property is an integer that is automatically incremented every time interval milliseconds pass. You can listen to this variable inside your app's callback to fire the callback on a predefined interval --> See following link for live updates in dash: [link](https://dash.plotly.com/live-updates).<br />
- Use Flask_caching for memoization:<br />
This can be used to store data in cache (filesystem/redis) for 15 minutes in our case.