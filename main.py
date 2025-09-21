import os
import requests
import json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine


API_KEY = "58c01c3fdbd8ace15f6a877a3a325552"  
CITIES = ["Dhaka", "Chittagong", "London", "New York", "Tokyo"]


DB_USER = "postgres"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "weather_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name):
  
    params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        print(f"Successfully fetched data for {city_name}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city_name}: {e}")
        return None

def save_raw_data(data, city_name):
   
    if data:
        today_str = datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join("data", "raw", today_str)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{city_name.lower()}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved raw data for {city_name}")


def transform_data(raw_data):
   
    city = raw_data['name']
    country = raw_data['sys']['country']
    weather_description = raw_data['weather'][0]['description']
    temperature = raw_data['main']['temp']
    feels_like = raw_data['main']['feels_like']
    humidity = raw_data['main']['humidity']
    wind_speed = raw_data['wind']['speed']
    observation_timestamp = datetime.utcfromtimestamp(raw_data['dt'])

    transformed_data = {
        'city': city,
        'country': country,
        'weather_description': weather_description,
        'temperature_celsius': temperature,
        'feels_like_celsius': feels_like,
        'humidity_percent': humidity,
        'wind_speed_mps': wind_speed,
        'observation_timestamp': observation_timestamp
    }
    return transformed_data

def load_data_to_db(df):
   
    try:
        engine = create_engine(DATABASE_URL)
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        print("Successfully loaded data to the database.")
    except Exception as e:
        print(f"Error loading data to database: {e}")

if __name__ == "__main__":
    print("Pipeline started...")
    all_cities_transformed_data = []
    
    for city in CITIES:
        weather_data = get_weather_data(city)
        if weather_data:
            save_raw_data(weather_data, city)
            transformed_data = transform_data(weather_data)
            all_cities_transformed_data.append(transformed_data)
    
    if all_cities_transformed_data:
        final_df = pd.DataFrame(all_cities_transformed_data)
        print("\n--- Transformed Data ---")
        print(final_df)
        
        load_data_to_db(final_df)
        
    print("Pipeline finished.")