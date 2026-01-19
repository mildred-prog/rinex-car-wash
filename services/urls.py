from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='list'),
    path("<int:pk>/", views.service_detail, name="detail"),
    path("ajax/load-tiers/", views.load_service_tiers, name="load_tiers"),

]


