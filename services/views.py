from django.shortcuts import render, get_object_or_404
from .models import Service


def services_list(request):
    """
    Display all active services grouped by category.
    """
    services = Service.objects.filter(is_active=True)

    # Optional: filter by category via querystring ?category=car
    category = request.GET.get("category")
    if category:
        services = services.filter(category=category)

    return render(request, "services/services_list.html", {
        "services": services,
        "active_category": category,
    })


def service_detail(request, pk):
    """
    Display a single service.
    """
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, "services/service_detail.html", {"service": service})
