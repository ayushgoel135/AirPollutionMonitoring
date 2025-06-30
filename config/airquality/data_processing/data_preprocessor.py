import pandas as pd
import numpy as np

def preprocess_data(df):
    # Handle missing values
    df = df.dropna()
    
    # Normalize features
    numeric_cols = ['aod', 'humidity', 'temperature', 'wind_speed']
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    
    return df