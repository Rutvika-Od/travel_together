from django.db import models
from django.contrib.auth.models import User


class DriverProfile(models.Model):
    VERIFICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50)
    license_image = models.ImageField(upload_to='licenses/')
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    car_color = models.CharField(max_length=30, blank=True)
    car_rc_document = models.FileField(upload_to='rc_documents/')
    insurance_document = models.FileField(upload_to='insurance/')
    verification_status = models.CharField(max_length=15, choices=VERIFICATION_STATUS, default='pending')
    total_rides = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.car_model} ({self.car_number})"

    def is_verified(self):
        return self.verification_status == 'verified'
