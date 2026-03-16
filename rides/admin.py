from django.contrib import admin
from .models import Ride, RideRequest, RideMessage, Notification

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'driver', 'price_per_seat', 'available_seats', 'status', 'departure_datetime']
    list_filter = ['status']
    search_fields = ['start_city', 'destination_city', 'driver__username']

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ['passenger', 'ride', 'status', 'seats_requested', 'requested_at']
    list_filter = ['status']

admin.site.register(RideMessage)
admin.site.register(Notification)
