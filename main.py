import requests
import csv
from datetime import datetime
import time
import schedule

API_key = 'bfe3a84c8d97d18cfc227e3ef0ca3317'

city_name = 'London'
state_code = ''
country_code = 'GB'
limit = 5
location_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_key}'

custom_file_name = 'weather_data.csv'

def get_weather_data():
    response = requests.get(url=location_url)  # Move this line inside the function
    if response.status_code == 200:
        location_data = response.json()

        for location in location_data:
            print(
                f'Location: {location["name"]}, Country: {location["country"]}, Lat: {location["lat"]}, Lon: {location["lon"]}')
    else:
        print(f'Failed to fetch location data. Status code: {response.status_code}')
        return

    lat = location_data[0]["lat"]
    lon = location_data[0]["lon"]

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    weather_response = requests.get(url=weather_url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature_kelvin = (weather_data["main"]["temp"])
        temperature_celsius = temperature_kelvin - 273.15
        weather_description = weather_data["weather"][0]["description"].upper()
        wind_speed = weather_data["wind"]["speed"]
        timezone = weather_data["name"]
        sunrise_time_unix = weather_data["sys"]["sunrise"]
        sunset_time_unix = weather_data["sys"]["sunset"]
        sunrise_time = datetime.utcfromtimestamp(sunrise_time_unix).strftime('%Y-%m-%d %H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(sunset_time_unix).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Temperature: {temperature_celsius:.2f}°C')
        print(f'Weather Description: {weather_description}')
        print(f'Wind Speed: {wind_speed}')
        print(f'Sunrise Time: {sunrise_time}')
        print(f'Sunset Time: {sunset_time}')
        print(timezone)

        with open(custom_file_name, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ['Location', 'Country', 'Latitude', 'Longitude', 'Temperature (°C)', 'Weather Description', 'Wind Speed',
                'Sunrise Time', 'Sunset Time'])
            writer.writerow(
                [location_data[0]["name"], location_data[0]["country"], location_data[0]["lat"], location_data[0]["lon"],
                f'{temperature_celsius:.2f}', weather_description, wind_speed, sunrise_time, sunset_time])

    else:
        print('Error fetching weather data. Status code:', weather_response.status_code)

# Schedule the job to run every 10 seconds
schedule.every(1).minute.do(get_weather_data)

# Infinite loop to execute scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
