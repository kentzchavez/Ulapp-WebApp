import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import numpy as np

def gen_preci_temp(weather_data):
    # Dictionary to store forecast data for each day
    daily_forecast = {}

    # Get today's date
    today = datetime.now().date()

    # Extracting forecast data
    forecasts = weather_data.get('list', [])

    for forecast in forecasts:
        date_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date = date_time.date()

        # Check if the date is within the range (past 4 days, current day, next 5 days)
        days_difference = (date - today).days

        if -4 <= days_difference <= 5:
            temperature = forecast['main']['temp']
            weather_desc = forecast['weather'][0]['main']
            probability_of_precipitation = forecast['pop'] * 100  # Probability of precipitation (%)

            # Create or update forecast data for each day
            if date not in daily_forecast:
                daily_forecast[date] = {'temperatures': [], 'conditions': [], 'precipitation': []}

            # Append temperature, condition, and probability of precipitation for each day
            daily_forecast[date]['temperatures'].append(temperature)
            daily_forecast[date]['conditions'].append(weather_desc)
            daily_forecast[date]['precipitation'].append(probability_of_precipitation)

    # Data visualization - Weather patterns over the 10-day period with circle sizes indicating precipitation probability
    plt.figure(figsize=(11.21, 3.92))

    for date, forecast_data in daily_forecast.items():
        temperatures = forecast_data['temperatures']
        conditions = forecast_data['conditions']
        precipitation = forecast_data['precipitation']

        # Check if any of the arrays is empty
        if not temperatures or not conditions or not precipitation:
            continue

        # Handle division by zero or NaN values during normalization
        try:
            # Normalize the temperatures for color gradient
            norm_temperatures = (np.array(temperatures) - min(temperatures)) / max(1, (max(temperatures) - min(temperatures)))
            norm_precipitation = (np.array(precipitation) - min(precipitation)) / max(1, (max(precipitation) - min(precipitation)))
        except (ValueError, ZeroDivisionError):
            continue

        # Calculate circle sizes based on probability of precipitation
        circle_sizes = 100 + (norm_precipitation * 500)  # Varying circle sizes between 100 and 600

        # Create gradient colors based on weather condition
        colors = []
        for condition in conditions:
            if condition == 'Clear':
                colors.append(mcolors.to_rgba('gold', alpha=0.6))
            elif condition == 'Clouds':
                colors.append(mcolors.to_rgba('lightgrey', alpha=0.6))
            elif condition == 'Rain':
                colors.append(mcolors.to_rgba('lightskyblue', alpha=0.6))

        # Plotting temperatures with gradient colors and varied circle sizes for precipitation probability
        plt.scatter([date] * len(temperatures), temperatures, c=colors, s=circle_sizes, edgecolor='black', linewidth=0.5)

    plt.title(f"Weather Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot as an image
    image_path = 'static/preci_temp_graph.png'
    plt.savefig(image_path)

    # Close the plot to free up resources
    plt.close()

    return
