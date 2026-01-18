from django.shortcuts import render

# Create your views here.

def services_list(request):
    return render(request, 'services/services.html')
