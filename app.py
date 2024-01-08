import pandas as pd
import plotly.express as px  # type: ignore
import plotly.utils  # type: ignore
import os

from utils.methods import *  # type: ignore
from flask import Flask, render_template, request, session
from flask_mail import Mail, Message  # type: ignore
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()
api_ipgeo_key = os.getenv("API_IPGEO_KEY")
api_google_key = os.getenv("API_GOOGLE_KEY")
api_weatherapi_key = os.getenv("API_WEATHERAPI_KEY")
mail_password = os.getenv("MAIL_PASSWORD")
mail_username = os.getenv("MAIL_USERNAME")
ip_api_key = os.getenv("IP_API_KEY")

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("API_SECRET")
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route('/')
def index():
    """Renders the index page"""
    return render_template('index.html', **locals())


@app.route('/about')
def about():
    """Renders the about page"""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Sends contact form and renders the index page"""
    if request.method == 'POST':
        msg = Message("Contact Form from DX-Dash",
                      sender=request.form.get('name'),
                      recipients=["dx-dash@mailtrap.io"])
        msg.body = """From: {} <{}>
        To: DX-Dash <dx-dash@mailtrap.io>
        Subject: New contact for DX-Dash
        {}""".format(request.form.get('name'), request.form.get('email'), request.form.get('message'))
        mail.send(msg)
    return render_template('index.html')


@app.route('/get_location', methods=['POST'])
def get_location():
    if request.method == 'POST':
        geolocator = Nominatim(user_agent="app")
        latitude = request.values.get('Latitude')
        longitude = request.values.get('Longitude')
        location = geolocator.reverse(latitude + "," + longitude, language='en')
        session['location'] = location.raw['address']
        print("result:", session['location'])
        return '', 204


@app.route('/home', methods=["GET"])
def home():
    """Renders the home page for current location at local time"""
    # Get actual time
    dt = datetime.datetime.now()
    # Get location from ip address
    location_info = {}
    if 'location' in session:
        location_info['city'] = session['location']['city']
        location_info['country'] = session['location']['country']
    # Reformat location to render title
    location = f'{location_info["city"]} - {location_info["country"]}'
    # Get full scope weather with weatherapi
    weather = get_weather(api_weatherapi_key, location_info['city'])
    # Get basic astrological info for current location at local time
    sunrise, sunset = get_astro(weather)
    # Get list for actual temperature, how does it feel like, air quality index and air quality description
    quality = get_quality(weather)
    # Get temperature forecast for next 3 days with weather icons
    weather_days = forecast_days(dt, weather)
    # Get weather forecast for next 24 hours with weather icons
    weather_hours = forecast_hours(dt, weather)
    # Get forecast for specific parameters
    params = forecast_params(weather)
    # Get alerts if any (modal as flag; if true, alerts are found)
    modal, alerts = get_alerts(weather)
    # Get embedded map link
    map_link = get_map_link(api_google_key, location_info['city'])
    # Get summary for city through teleport api
    summary = get_summary(location_info['city'].lower())
    return render_template("home.html", air_q_index=quality[2], air_q_desc=quality[3], summary=summary,
                           temp=quality[0], feels=quality[1], map_link=map_link, sunrise=sunrise, sunset=sunset,
                           location=location, weather_hours=weather_hours, weather_days=weather_days,
                           params=params, alerts=[alerts[0], alerts[1], alerts[2]], modal=modal)


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    """Renders the explore page for weather in other locations around the globe"""
    if request.method == 'POST' and request.form['search'] == 'search':
        # Get actual time
        dt = datetime.datetime.now()
        # Get current location as a dictionary
        # location_info = get_location('50.937531', '6.960279')

        location_info = get_location_from_ip(ip_api_key)

        # Get current city of user
        current_city = location_info['city']
        # Get full scope weather with weatherapi
        weather = get_weather(api_weatherapi_key, request.form['city'])
        # Get basic astrological info for current location at local time
        sunrise, sunset = get_astro(weather)
        # Get list for actual temperature, how does it feel like, air quality index and air quality description
        quality = get_quality(weather)
        # Get actual time in user location
        time_in_current_location = get_timezone(current_city).localize(dt)
        # Get actual time in searched city
        time_in_city = time_in_current_location.astimezone(get_timezone(request.form['city'].split(',')[0]))
        # Get temperature forecast for next 3 days with weather icons
        weather_days = forecast_days(time_in_city, weather)
        # Get weather forecast for next 24 hours with weather icons
        weather_hours = forecast_hours(dt, weather)
        # Get forecast for specific parameters
        params = forecast_params(weather)
        # Get alerts if any (modal as flag; if true, alerts are found)
        modal, alerts = get_alerts(weather)
        # Get embedded map link
        map_link, flag = get_src(api_google_key, request.form['city'].split(', ')[0].lower())
        # Get summary for city through teleport api
        summary = get_summary(request.form['city'].split(', ')[0].lower())
        # ------------ PLOTS ------------ #
        # Get weather for hours as dataframe
        df = pd.DataFrame.from_dict(weather_hours)
        # Transpose dataframe
        df_transposed = df.T
        # Change type to numerics
        df_transposed['temperature'] = df_transposed['temperature'].apply(pd.to_numeric)
        df_transposed['humidity'] = df_transposed['humidity'].apply(pd.to_numeric)
        # Extract values for temperature and humidity
        dc_temp = df_transposed['temperature']
        dc_humidity = df_transposed['humidity']
        # Create figure 1 with suitable layout update
        fig1 = px.line(dc_temp, title='Temperature forecast in <i>degrees</i>')
        fig1.update_traces(line_color='yellow')
        fig1.update_layout(
            paper_bgcolor='rgba(33, 37, 41, 0.3)',
            plot_bgcolor='rgba(33, 37, 41, 0.05)',
            font_color="white",
            yaxis_title="",
            xaxis_title="",
            showlegend=False,
            margin=dict(l=5, r=5, t=50, b=5),
            font=dict(size=16, color="yellow"))
        fig1.update_xaxes(mirror=True, ticks='outside', showline=True, gridcolor='lightgrey')
        fig1.update_yaxes(mirror=True, ticks='outside', showline=True, gridcolor='lightgrey')
        # Create figure 2 with suitable layout update
        fig2 = px.line(dc_humidity, title='Humidity forecast in <i>percent</i>')
        fig2.update_traces(line_color='darkturquoise')
        fig2.update_layout(
            paper_bgcolor='rgba(33, 37, 41, 0.3)',
            plot_bgcolor='rgba(33, 37, 41, 0.05)',
            font_color="white",
            yaxis_title="",
            xaxis_title="",
            showlegend=False,
            margin=dict(l=5, r=5, t=50, b=5),
            font=dict(size=16, color="darkturquoise"))
        fig2.update_xaxes(mirror=True, ticks='outside', showline=True, gridcolor='lightgrey')
        fig2.update_yaxes(mirror=True, ticks='outside', showline=True, gridcolor='lightgrey')
        # Create Graph Json objects to render
        graph1json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graph2json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('explore.html', air_q_index=quality[2], air_q_desc=quality[3], temp=quality[0],
                               feels=quality[1], sunrise=sunrise, sunset=sunset, summary=summary,
                               location=request.form['city'], flag=flag,
                               map_link=map_link, weather_hours=weather_hours, weather_days=weather_days,
                               params=params, alerts=[alerts[0], alerts[1], alerts[2]], modal=modal,
                               graph1json=graph1json,
                               graph2json=graph2json)
    return render_template('explore.html')


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
