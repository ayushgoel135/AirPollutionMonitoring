import os
import json
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import certifi
from config.settings import MONGO_URI, MONGO_DB_NAME

def load_sample_data():
    client = MongoClient(MONGO_URI,
                         tls=True,
                         tlsCAFile=certifi.where(),  # Use system CA certificates
                         connectTimeoutMS=30000,
                         socketTimeoutMS=30000)
    db = client[MONGO_DB_NAME]
    
    # Clear existing data
    db.satellite_data.drop()
    db.ground_measurements.drop()
    db.predictions.drop()
    
    # Indian cities with coordinates
    indian_cities = [
        {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
        {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
        {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
        {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
        {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
        {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462}
    ]
    
    # Generate 30 days of data
    for i in range(30):
        date = datetime.now() - timedelta(days=30 - i)
        
        for city in indian_cities:
            # Satellite data (AOD)
            aod = round(random.uniform(0.1, 1.5), 2)
            humidity = random.randint(30, 90)
            temperature = random.randint(15, 40)
            wind_speed = round(random.uniform(1, 15), 1)
            
            sat_data = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "aod": aod,
                "humidity": humidity,
                "temperature": temperature,
                "wind_speed": wind_speed,
                "timestamp": date.isoformat()
            }
            db.satellite_data.insert_one(sat_data)
            
            # Ground measurements (PM2.5) - correlated with AOD but with some noise
            pm25 = round((aod * 30) + random.uniform(-5, 5), 2)
            if pm25 < 0: pm25 = 0
            
            ground_data = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "pm2_5": pm25,
                "timestamp": date.isoformat(),
                "location": city["name"]
            }
            db.ground_measurements.insert_one(ground_data)
            
            # Predictions - similar to ground truth but with some error
            predicted_pm25 = round(pm25 + random.uniform(-2, 2), 2)
            if predicted_pm25 < 0: predicted_pm25 = 0
            
            prediction_data = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "pm2_5": predicted_pm25,
                "timestamp": date.isoformat(),
                "location": city["name"],
                "aod": aod,
                "humidity": humidity,
                "temperature": temperature,
                "wind_speed": wind_speed
            }
            db.predictions.insert_one(prediction_data)
    
    print("Sample data loaded successfully")

if __name__ == "__main__":
    load_sample_data()