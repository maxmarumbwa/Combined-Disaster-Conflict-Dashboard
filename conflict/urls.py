from django.urls import path
from . import views

urlpatterns = [
    path("map/", views.displacement_map, name="displacement_map"),
    path("geojson/", views.displacement_geojson, name="displacement_geojson"),
]
