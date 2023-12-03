import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz

API_KEY = 'c3ab9a2a4ccfaac2065c44ce3977630b'

def get_5_day_forecast(city_name):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_nearest_forecast(weather_data):
    if weather_data and 'list' in weather_data and weather_data['list']:
        current_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        nearest_forecast = min(weather_data['list'], key=lambda x: abs(pd.Timestamp(x['dt_txt']) - pd.Timestamp(current_time)))
        return [nearest_forecast]
    return []

def convert_utc_to_local(utc_time, timezone):
    utc_datetime = datetime.utcfromtimestamp(utc_time).replace(tzinfo=pytz.utc)
    local_datetime = utc_datetime.astimezone(pytz.timezone(timezone))
    return local_datetime.strftime('%Y-%m-%d %H:%M:%S')

def display_5_day_forecast(data):
    if data:
        city = data['city']['name']
        forecast_list = data['list']

        current_day = None
        day_counter = 0

        for item in forecast_list:
            timestamp = item['dt_txt']
            date = timestamp.split()[0]

            if date != current_day:
                if current_day is not None:
                    print(f"Day {day_counter}:")
                    if 'sys' in current_day:
                        print(f"Sunrise: {convert_utc_to_local(current_day['sys'].get('sunrise', 0), data['city']['timezone'])}")
                        print(f"Sunset: {convert_utc_to_local(current_day['sys'].get('sunset', 0), data['city']['timezone'])}")
                    else:
                        print("No sunrise/sunset data available.")
                    print("\n")

                current_day = date
                day_counter += 1

            day_data = {
                'Date & Time': timestamp,
                'Temperature (°C)': item['main']['temp'],
                'Description': item['weather'][0]['description'],
                'Cloudiness (%)': item['clouds']['all'],
                'Humidity (%)': item['main']['humidity'],
                'Wind Speed (m/s)': item['wind']['speed'],
                'Rain (3h) (mm)': item.get('rain', {}).get('3h', 0),
                'Sunrise': item['sys'].get('sunrise', 'N/A'),
                'Sunset': item['sys'].get('sunset', 'N/A')
            }

            print(f"Date & Time: {timestamp}")
            print(f"Temperature: {day_data['Temperature (°C)']}°C")
            print(f"Description: {day_data['Description']}")
            print(f"Cloudiness: {day_data['Cloudiness (%)']}%")
            print(f"Humidity: {day_data['Humidity (%)']}%")
            print(f"Wind Speed: {day_data['Wind Speed (m/s)']} m/s")
            print(f"Rain (3h): {day_data['Rain (3h) (mm)']} mm")
            print(f"Sunrise: {convert_utc_to_local(day_data['Sunrise'], data['city']['timezone'])}")
            print(f"Sunset: {convert_utc_to_local(day_data['Sunset'], data['city']['timezone'])}\n")

    else:
        print("No data found :(")

if __name__ == '__main__':
    print('Ulapp Forecasting(BETA)')
    city_name = input("Enter city name: ")
    forecast_data = get_5_day_forecast(city_name)
    display_5_day_forecast(forecast_data)
