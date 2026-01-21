from django.urls import path
from . import views

urlpatterns = [
    path("map/", views.displacement_map, name="displacement_map"),
    path("geojson/", views.displacement_geojson, name="displacement_geojson"),
    path("add/", views.add_displacement_event, name="add_displacement_event"),
    path("upload-csv/", views.upload_displacement_csv, name="upload_displacement_csv"),
    path(
        "upload_political_violence/",
        views.upload_political_violence,
        name="upload_political_violence",
    ),
    path(
        "add_political_violence/",
        views.add_political_violence_record,
        name="add_political_violence_record",
    ),
    path(
        "fatalities/province/<int:province_id>/",
        views.fatalities_timeseries,
        name="fatalities_timeseries",
    ),
]
