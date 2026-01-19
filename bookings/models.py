from django.db import models
from services.models import Service, ServiceTier


class Booking(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bookings")
    tier = models.ForeignKey(ServiceTier, on_delete=models.PROTECT, null=True, blank=True)

    property_or_vehicle = models.CharField(max_length=120, blank=True)  # e.g. "SUV", "2-bed flat"
    postcode = models.CharField(max_length=20)

    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Optional for future: status tracking (good for operations)
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return f"{self.full_name} | {self.service.name}"
