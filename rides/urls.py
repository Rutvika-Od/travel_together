from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_rides, name='search_rides'),
    path('my/', views.my_rides, name='my_rides'),
    path('create/', views.create_ride, name='create_ride'),
    path('<int:pk>/', views.ride_detail, name='ride_detail'),
    path('<int:pk>/edit/', views.edit_ride, name='edit_ride'),
    path('<int:pk>/delete/', views.delete_ride, name='delete_ride'),
    path('<int:pk>/request/', views.request_ride, name='request_ride'),
    path('<int:pk>/manage/', views.manage_requests, name='manage_requests'),
    path('<int:pk>/manage/<int:req_id>/<str:action>/', views.update_request, name='update_request'),
    path('cancel/<int:pk>/', views.cancel_request, name='cancel_request'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/count/', views.get_unread_count, name='unread_count'),
]
