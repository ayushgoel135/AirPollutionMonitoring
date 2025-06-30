from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from airquality.models import SatelliteData, GroundMeasurement
from config.settings import ML_MODEL_PATH
from ..data_processing.data_loader import load_and_process_data
from ..data_processing.data_preprocessor import preprocess_data
import os

def train_and_save_model(X, y):
    # Preprocess data
    df = pd.concat([X, y], axis=1)
    df = preprocess_data(df)
    X = df.drop('pm2_5', axis=1)
    y = df['pm2_5']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Save model
    os.makedirs(os.path.dirname(ML_MODEL_PATH), exist_ok=True)
    joblib.dump(model, ML_MODEL_PATH)
    
    return r2  # Return R-squared score as accuracy metric