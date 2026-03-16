from django.db import models
from django.contrib.auth.models import User


class Ride(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('full', 'Full'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver')
    start_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=3)
    available_seats = models.PositiveIntegerField(default=3)
    pickup_points = models.TextField(blank=True, help_text='Comma-separated pickup points')
    drop_points = models.TextField(blank=True, help_text='Comma-separated drop points')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-departure_datetime']

    def __str__(self):
        return f"{self.start_city} → {self.destination_city} | {self.departure_datetime.strftime('%d %b %Y')}"

    def get_pickup_list(self):
        if self.pickup_points:
            return [p.strip() for p in self.pickup_points.split(',') if p.strip()]
        return []

    def get_drop_list(self):
        if self.drop_points:
            return [p.strip() for p in self.drop_points.split(',') if p.strip()]
        return []

    def approved_passengers(self):
        return self.requests.filter(status='approved')

    def is_full(self):
        return self.available_seats <= 0


class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_requests')
    seats_requested = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['ride', 'passenger']
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.passenger.username} → {self.ride} [{self.status}]"


class RideMessage(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"


class Notification(models.Model):
    NOTIF_TYPES = [
        ('ride_request', 'Ride Request'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected'),
        ('new_message', 'New Message'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_notifications')
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    message = models.CharField(max_length=300)
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
