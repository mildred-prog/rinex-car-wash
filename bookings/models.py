from django.db import models
from django.conf import settings
from services.models import Service, ServiceTier


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bookings")
    tier = models.ForeignKey(ServiceTier, on_delete=models.PROTECT, null=True, blank=True)

    property_or_vehicle = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=20)

    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return f"{self.full_name} | {self.service.name}"
