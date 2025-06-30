from django.shortcuts import render
from .models import SatelliteData, GroundMeasurement, Prediction
from .ml_model.train_model import train_and_save_model
from .data_processing.data_loader import load_and_process_data
import json
from django.http import JsonResponse

def index(request):
    return render(request, 'airquality/index.html')

def dashboard(request):
    predictions = Prediction.get_latest_predictions()
    
    # Convert ObjectId to string for JSON serialization
    for pred in predictions:
        pred['_id'] = str(pred['_id'])
    
    context = {
        'predictions': json.dumps(predictions)
    }
    return render(request, 'airquality/dashboard.html', context)

def update_model(request):
    if request.method == 'POST':
        try:
            # Load and process new data
            X, y = load_and_process_data()
            
            # Train and save the model
            accuracy = train_and_save_model(X, y)
            
            return JsonResponse({
                'status': 'success',
                'accuracy': accuracy
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_predictions(request):
    predictions = Prediction.get_latest_predictions()
    
    # Convert ObjectId to string for JSON serialization
    for pred in predictions:
        pred['_id'] = str(pred['_id'])
    
    return JsonResponse({
        'status': 'success',
        'data': predictions
    })