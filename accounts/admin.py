from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'is_driver', 'verification_status']
    list_filter = ['verification_status', 'is_driver']
    actions = ['verify_users', 'reject_users']

    def verify_users(self, request, queryset):
        queryset.update(verification_status='verified')
    verify_users.short_description = 'Mark selected as Verified'

    def reject_users(self, request, queryset):
        queryset.update(verification_status='rejected')
    reject_users.short_description = 'Mark selected as Rejected'
