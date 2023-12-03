import requests
from modules.weather_api.ulapp_api import API_KEY

def get_location_data(city_name):
    base_url = 'http://api.openweathermap.org/geo/1.0/direct'
    
    params = {
        'q': city_name,
        'appid': API_KEY,
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_lat_lon(data):
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        print("Error: Location data is empty.")
        return None, None

def get_pollution_data(lat, lon):
    base_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_air_quality(pollution_data):
    if pollution_data and 'list' in pollution_data and pollution_data['list']:
        return pollution_data['list'][0]['main']['aqi']
    else:
        print("Error: Unable to get air quality data.")
        return None

if __name__ == '__main__':
    print('Ulapp Forecasting(BETA)')
    city_name = input("Enter city name: ")
    location_data = get_location_data(city_name)
    
    if location_data:
        lat, lon = get_lat_lon(location_data)
        
        if lat is not None and lon is not None:
            pollution_data = get_pollution_data(lat, lon)
            
            if pollution_data:
                air_quality = get_air_quality(pollution_data)
                if air_quality is not None:
                    print(f"Air Quality Index: {air_quality}")
            else:
                print("Error fetching pollution data.")
        else:
            print("Error fetching location coordinates.")
    else:
        print("Error fetching location data.")
