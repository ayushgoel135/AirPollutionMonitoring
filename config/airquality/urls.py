from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/update_model/', views.update_model, name='update_model'),
    path('api/get_predictions/', views.get_predictions, name='get_predictions'),
]