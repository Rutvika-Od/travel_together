from django.urls import path
from . import views

urlpatterns = [
    path('become/', views.become_driver, name='become_driver'),
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),
]
