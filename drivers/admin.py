from django.contrib import admin
from .models import DriverProfile

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'car_model', 'car_number', 'verification_status', 'total_rides', 'rating']
    list_filter = ['verification_status']
    actions = ['verify_drivers', 'reject_drivers']

    def verify_drivers(self, request, queryset):
        queryset.update(verification_status='verified')
    verify_drivers.short_description = 'Verify selected drivers'

    def reject_drivers(self, request, queryset):
        queryset.update(verification_status='rejected')
    reject_drivers.short_description = 'Reject selected drivers'
