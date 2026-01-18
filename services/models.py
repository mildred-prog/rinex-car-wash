from django.db import models


class Service(models.Model):
    CATEGORY_CHOICES = [
        ("car", "Car Care"),
        ("home", "Home Cleaning"),
        ("commercial", "Office & Shop Cleaning"),
        ("move", "Move In / Move Out"),
        ("upholstery", "Upholstery & Fabrics"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Copy for website/flyer
    short_description = models.CharField(max_length=255)
    full_description = models.TextField(blank=True)

    # Base pricing anchor (useful even if tiers exist)
    starting_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Starting price in GBP"
    )

    # Useful for service cards + filtering
    ideal_for = models.CharField(max_length=100, help_text="e.g., Vehicle / Home / Business")

    # Controls what appears on the homepage “snapshot”
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class ServiceTier(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tiers")
    label = models.CharField(max_length=120)  # e.g. "Small car", "2-bed home"
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # optional: for "Quote required" or notes
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["price", "label"]

    def __str__(self):
        return f"{self.service.name} - {self.label}"
