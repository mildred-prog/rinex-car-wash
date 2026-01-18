from django.contrib import admin
from .models import Service, ServiceTier


class ServiceTierInline(admin.TabularInline):
    model = ServiceTier
    extra = 3


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "starting_price", "is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name", "short_description", "full_description")
    inlines = [ServiceTierInline]
