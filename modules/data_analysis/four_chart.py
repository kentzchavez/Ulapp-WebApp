import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

def generate_temp_hum_line_graph(weather_data):
    # Lists to store date, temperature, humidity, rain, and windspeed data
    dates = []
    temperatures = []
    humidity_values = []
    rain_values = []
    windspeed_values = []

    # Extracting forecast data
    forecasts = weather_data.get('list', [])

    print("Number of forecasts:", len(forecasts))  # Debug print

    for forecast in forecasts:
        # Extract date, temperature, humidity, rain, and windspeed for each forecast
        date_str = forecast.get('dt_txt', '')
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        temperature = forecast.get('main', {}).get('temp')
        humidity = forecast.get('main', {}).get('humidity')
        rain = forecast.get('rain', {}).get('3h', 0)
        windspeed = forecast.get('wind', {}).get('speed')

        # Ensure that temperature, humidity, rain, and windspeed are not None
        if all(val is not None for val in [temperature, humidity, rain, windspeed]):
            dates.append(date_time)
            temperatures.append(temperature)
            humidity_values.append(humidity)
            rain_values.append(rain)
            windspeed_values.append(windspeed)

    print("Number of valid data points:", len(dates))  # Debug print

    # Data visualization - Temperature, Humidity, Rain, and Windspeed over time
    plt.figure(figsize=(11.21, 3.92))  # Set the width and height in inches

    # Plotting temperatures with the specified line color
    plt.plot(dates, temperatures, linestyle='-', marker='o', color='#453297', label='Temperature (°C)')

    # Plotting humidity values with a different line color
    plt.plot(dates, humidity_values, linestyle='-', marker='o', color='#1f77b4', label='Humidity (%)')

    # Plotting rain values with another line color
    plt.plot(dates, rain_values, linestyle='-', marker='o', color='#9400D3', label='Rain (3h) (mm)')

    # Plotting windspeed values with the specified light blue color
    plt.plot(dates, windspeed_values, linestyle='-', marker='o', color='#ADD8E6', label='Windspeed (m/s)')

    # Adding labels and title
    plt.title(f"Forecast Correlational Chart for {weather_data.get('city', {}).get('name')}")
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot as an image
    image_path = 'static/temp_hum_rain_wind_graph.png'  # Adjust the path as needed
    plt.savefig(image_path)

    # Close the plot to free up resources
    plt.close()

    return image_path
