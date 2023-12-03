import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

def generate_temperature_line_graph(weather_data):
    # Lists to store date and temperature data
    dates = []
    temperatures = []

    # Extracting forecast data
    forecasts = weather_data.get('list', [])

    print("Number of forecasts:", len(forecasts))  # Debug print

    for forecast in forecasts:
        # Extract date and temperature for each forecast
        date_str = forecast.get('dt_txt', '')
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        temperature = forecast.get('main', {}).get('temp')

        # Ensure that temperature is not None
        if temperature is not None:
            dates.append(date_time)
            temperatures.append(temperature)

    print("Number of valid temperatures:", len(temperatures))  # Debug print

    # Data visualization - Temperature over time
    plt.figure(figsize=(11.21, 3.92))  # Set the width and height in inches

    # Plotting temperatures with the specified line color
    plt.plot(dates, temperatures, linestyle='-', marker='o', color='#453297', label='Temperature (°C)')

    # Adding labels and title
    plt.title(f"Temperature Forecast for {weather_data.get('city', {}).get('name')}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot as an image
    image_path = 'static/temperature_graph.png'  # Adjust the path as needed
    plt.savefig(image_path)

    # Close the plot to free up resources
    plt.close()

    return image_path
