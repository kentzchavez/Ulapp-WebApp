from flask import Flask, render_template, request
from modules.Ai_News_Section.get_articles import get_articles
from modules.weather_api.ulapp_api import get_5_day_forecast
from modules.uv_sun_fetch.get_uv import get_uv_sunset_sunrise  # Update the import statement
import datetime

app = Flask(__name__)

# Set the default city
default_city = "Manila"  # You can change this to your preferred default city

def get_nearest_forecast(weather_data):
    # Assuming weather_data['list'] is a list of forecasts
    if weather_data and 'list' in weather_data and weather_data['list']:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nearest_forecast = min(weather_data['list'], key=lambda x: abs(datetime.datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')))
        return [nearest_forecast]
    return []

def get_uv_sunset_sunrise_data(city):
    # Get your API key from the WeatherAPI website and replace 'YOUR_API_KEY' below
    api_key = '190764b3a60b469fa8b143518231711'
    return get_uv_sunset_sunrise(api_key, city)

@app.route('/')
def index():
    global default_city  # Declare the default_city as a global variable

    city_query = request.args.get('city', default_city)  # Use the default city if not provided in the URL

    # Get articles data
    articles_data = get_articles()

    # Get weather data using ulapp_api.py if a city is specified
    weather_data = None
    uv_sunset_sunrise_data = None

    if city_query:
        weather_data = get_5_day_forecast(city_query)

        # Check if weather_data is not None before modifying it
        if weather_data:
            weather_data['list'] = get_nearest_forecast(weather_data)

            # Use the UV index API call
            uv_sunset_sunrise_data = get_uv_sunset_sunrise_data(city_query)

    return render_template('index.html', articles_data=articles_data, weather_data=weather_data, uv_sunset_sunrise_data=uv_sunset_sunrise_data)

if __name__ == '__main__':
    app.run(debug=True)
