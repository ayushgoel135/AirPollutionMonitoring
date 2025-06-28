import os
import json
import random
import certifi
from datetime import datetime, timedelta
from pymongo import MongoClient
import sys
from urllib.parse import quote_plus
import socket
import ssl

def test_dns_resolution(hostname):
    try:
        socket.gethostbyname(hostname)
        print(f"✅ {hostname} resolves")
        return True
    except Exception as e:
        print(f"❌ Cannot resolve {hostname}: {e}")
        return False

def create_mongo_client(connection_string, username=None, password=None):
    # Try multiple connection approaches
    attempts = [
        # Attempt 1: Full connection with TLS
        {
            "uri": connection_string,
            "params": {
                "tls": True,
                "tlsCAFile": certifi.where(),
                "serverSelectionTimeoutMS": 15000,
                "connectTimeoutMS": 15000,
                "socketTimeoutMS": 30000
            }
        },
        # Attempt 2: Without TLS (development only)
        {
            "uri": connection_string.replace("ssl=true", "ssl=false"),
            "params": {
                "serverSelectionTimeoutMS": 15000,
                "connectTimeoutMS": 15000
            }
        },
        # Attempt 3: Direct IP connection if DNS fails
        {
            "uri": connection_string.replace(
                "atlas-sql-680f6b1365053f71e0001481-w31smy.a.query.mongodb.net",
                "34.227.123.45"  # Replace with actual IP from nslookup
            ),
            "params": {
                "tls": True,
                "tlsCAFile": certifi.where(),
                "serverSelectionTimeoutMS": 15000
            }
        }
    ]
    
    for attempt in attempts:
        try:
            print(f"\nAttempting connection with: {attempt['uri'][:50]}...")
            #client = MongoClient(attempt["uri"], **attempt["params"])
            #client.admin.command('ping')
            username = "ayush"  # Replace with your username
            password = "ayush123"  # Replace with your password
            encoded_password = quote_plus(password)
            db_name = "sample_mflix"
            hostname="cluster0.pxafi1v.mongodb.net"
            MONGO_URI = f"mongodb+srv://{username}:{encoded_password}@{hostname}/{db_name}?retryWrites=true&w=majority"
            client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
            print("✅ Connection successful!")
            return client
        except Exception as e:
            print(f"⚠️ Attempt failed: {str(e)[:100]}...")
            continue
    
    raise Exception("All connection attempts failed")

def load_sample_data():
    client = None
    try:
        # 1. Configuration
        username = "ayush"  # Replace with your username
        password = "ayush123"  # Replace with your password
        encoded_password = quote_plus(password)
        db_name = "sample_mflix"
        
        # 2. Test DNS resolution first
        #hostname="cluster0.pxafi1v.mongodb.net"
        #hostname = "atlas-sql-680f6b1365053f71e0001481-w31smy.a.query.mongodb.net"
        hostname="cluster0.pxafi1v.mongodb.net"

        if not test_dns_resolution(hostname):
            # If DNS fails, try getting IP manually
            print("\n⚠️ DNS resolution failed. Trying to find IP address...")
            try:
                ip = socket.gethostbyname(hostname)
                print(f"Found IP: {ip}")
            except:
                print("Could not resolve IP. Check your internet connection.")
                return

        # 3. Create connection string
        #MONGO_URI = f"mongodb://{username}:{encoded_password}@{hostname}/{db_name}?ssl=true&authSource=admin"
        MONGO_URI = f"mongodb+srv://{username}:{encoded_password}@{hostname}/{db_name}?retryWrites=true&w=majority"

        
        # 4. Establish connection with fallback options
        client = create_mongo_client(MONGO_URI, username, password)
        
        # 5. Database operations
        db = client[db_name]
        
        # Clear existing collections safely
        collections = ['satellite_data', 'ground_measurements', 'predictions']
        for col in collections:
            try:
                db[col].drop()
                print(f"✅ Dropped collection: {col}")
            except:
                print(f"⚠️ Collection {col} doesn't exist or couldn't be dropped")

        # Indian cities with coordinates
        indian_cities =     [
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
        db.indian_cities.insert_many(indian_cities)
        # Generate 30 days of data
        print("\nGenerating sample data...")
        for i in range(30):
            date = datetime.now() - timedelta(days=30 - i)
            
            for city in indian_cities:
                # Common environmental factors
                aod = round(random.uniform(0.1, 1.5), 2)
                humidity = random.randint(30, 90)
                temperature = random.randint(15, 40)
                wind_speed = round(random.uniform(1, 15), 1)
                
                # Satellite data
                sat_data = {
                    "latitude": city["lat"],
                    "longitude": city["lon"],
                    "aod": aod,
                    "humidity": humidity,
                    "temperature": temperature,
                    "wind_speed": wind_speed,
                    "timestamp": date,
                    "location": city["name"]
                }
                db.satellite_data.insert_one(sat_data)
                
                # Ground measurements (PM2.5)
                pm25 = round((aod * 30) + random.uniform(-5, 5), 2)
                pm25 = max(0, pm25)
                
                ground_data = {
                    "latitude": city["lat"],
                    "longitude": city["lon"],
                    "pm2_5": pm25,
                    "timestamp": date,
                    "location": city["name"]
                }
                db.ground_measurements.insert_one(ground_data)
                
                # Predictions
                predicted_pm25 = round(pm25 + random.uniform(-2, 2), 2)
                predicted_pm25 = max(0, predicted_pm25)
                
                prediction_data = {
                    "latitude": city["lat"],
                    "longitude": city["lon"],
                    "pm2_5": predicted_pm25,
                    "timestamp": date,
                    "location": city["name"],
                    "aod": aod,
                    "humidity": humidity,
                    "temperature": temperature,
                    "wind_speed": wind_speed,
                    "ground_truth_pm2_5": pm25
                }
                db.predictions.insert_one(prediction_data)
            
            if (i + 1) % 5 == 0:
                print(f"Generated data for {i + 1} days")

        print("\n✅ Sample data loaded successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        if client:
            client.close()
            print("\nMongoDB connection closed")

if __name__ == "__main__":
    load_sample_data()

