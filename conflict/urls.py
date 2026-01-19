# urls.py
from django.urls import path
from .views import DisplacementGeoJSON
from . import views

urlpatterns = [
    path("displacements/map/", views.displacement_map, name="displacement_map"),
    path(
        "displacements/data/",
        DisplacementGeoJSON.as_view(),
        name="displacement_geojson",
    ),
]
