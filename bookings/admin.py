from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "service", "tier", "postcode", "preferred_date", "status", "created_at")
    list_filter = ("status", "service", "preferred_date", "created_at")
    search_fields = ("full_name", "phone", "email", "postcode", "message")
    ordering = ("-created_at",)
