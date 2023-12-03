from flask import Flask, render_template, request, redirect
from modules.Ai_News_Section.get_articles import get_articles
from modules.weather_api.ulapp_api import get_5_day_forecast
from modules.weather_api.get_pollution import get_location_data, get_lat_lon, get_pollution_data, get_air_quality
from modules.uv_sun_fetch.get_uv import get_weather_data
from modules.data_analysis.line_graph import generate_temperature_line_graph
from modules.data_analysis.preci_temp import gen_preci_temp
from modules.data_analysis.four_chart import generate_temp_hum_line_graph
import datetime

app = Flask(__name__)

# Set the default city
default_city = "Manila"  # You can change this to your preferred default city
weather_data = None
uv_hourly = None
temperature_graph_path = None

# File to store the last valid city
queries_file = "queries.txt"

def save_last_city(city):
    with open(queries_file, "w") as file:
        file.write(city)

def load_last_city():
    try:
        with open(queries_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return default_city

def get_nearest_forecast(weather_data):
    # Assuming weather_data['list'] is a list of forecasts
    if weather_data and 'list' in weather_data and weather_data['list']:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nearest_forecast = min(weather_data['list'], key=lambda x: abs(datetime.datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')))
        return [nearest_forecast]
    return []

def get_uv_hourly(city):
    # Get your API key from the WeatherAPI website and replace 'YOUR_API_KEY' below
    api_key = 'ffc8d6b52f90426db3b85632231911'
    return get_weather_data(api_key, city)

@app.route('/')
def index():
    global default_city, weather_data, uv_hourly, temperature_graph_path  # Declare global variables

    city_query = request.args.get('city', default_city)  # Use the default city if not provided in the URL

    # Get articles data
    articles_data = get_articles()

    # Initialize variables to None
    new_weather_data = get_5_day_forecast(city_query)

    # Get air quality
    location_data = get_location_data(city_query)
    lat, lon = get_lat_lon(location_data)
    pollution_data = get_pollution_data(lat, lon)
    air_quality_index = get_air_quality(pollution_data)

    # Check if new_weather_data is not None before modifying it
    if new_weather_data is not None:
        generate_temperature_line_graph(new_weather_data)
        gen_preci_temp(new_weather_data)
        generate_temp_hum_line_graph(new_weather_data)
        new_weather_data['list'] = get_nearest_forecast(new_weather_data)
        
        if new_weather_data['list'] is not None:
            # Use the UV index API call
            new_uv_hourly = get_uv_hourly(city_query)
            print("Length of hourly_forecast:", len(new_uv_hourly['hourly_forecast']))
            #print(new_uv_hourly)

            # Check if uv_hourly is not empty
            if new_uv_hourly['hourly_forecast'] is not None:
                # Update weather_data only if new data is available
                weather_data = new_weather_data
                uv_hourly = new_uv_hourly

                # Save the last valid city
                save_last_city(city_query)
    else:
        # Load the last valid city
        last_valid_city = load_last_city()
        return redirect(f'/?city={last_valid_city}')

    current_hour = datetime.datetime.now().hour
    return render_template('index.html', current_hour=current_hour, static_folder='public', static_url_path='/static', articles_data=articles_data, weather_data=weather_data, uv_hourly=uv_hourly, air_quality_index=air_quality_index)

if __name__ == '__main__':
    app.run(debug=True)
