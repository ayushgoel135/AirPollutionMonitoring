import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from ..models import SatelliteData, GroundMeasurement
import joblib
from config.settings import ML_MODEL_PATH
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os

def load_and_process_data():
    # Load satellite data
    satellite_data = SatelliteData.get_all_data()
    sat_df = pd.DataFrame(satellite_data)
    
    # Load ground measurements
    ground_data = GroundMeasurement.get_all_data()
    ground_df = pd.DataFrame(ground_data)
    
    # Merge datasets
    merged_df = pd.merge(sat_df, ground_df, on=['latitude', 'longitude', 'timestamp'])
    
    # Feature engineering
    X = merged_df[['aod', 'humidity', 'temperature', 'wind_speed']]
    y = merged_df['pm2_5']
    
    return X, y