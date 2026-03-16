from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    VERIFICATION_STATUS = [
        ('unverified', 'Unverified'),
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    verification_document = models.FileField(upload_to='verification/', blank=True, null=True)
    document_type = models.CharField(max_length=20, blank=True, choices=[
        ('aadhar', 'Aadhar Card'),
        ('pan', 'PAN Card'),
    ])
    verification_status = models.CharField(max_length=15, choices=VERIFICATION_STATUS, default='unverified')
    is_driver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_initials(self):
        name = self.user.get_full_name()
        if name:
            parts = name.split()
            return (parts[0][0] + parts[-1][0]).upper()
        return self.user.username[0].upper()
