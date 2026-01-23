from django.urls import path
from . import views

urlpatterns = [
    path(
        "upload_political_violence/",
        views.upload_political_violence,
        name="upload_political_violence",
    ),
    path("api/geojson/", views.political_violence_choropleth, name="choropleth_api"),
    path(
        "map/choropleth/",
        views.political_violence_choropleth_page,
        name="political_violence_choropleth",
    ),
    # path(
    #     "table/",
    #     views.political_violence_table,
    #     name="political_violence_table",
    # ),
    path(
        "api/table/",
        views.political_violence_table_api,
        name="political_violence_table_api",
    ),
]


# from django.urls import path
# from . import views
# from .views import fatalities_choropleth_map
# from .views import fatalities_choropleth_geojson

# urlpatterns = [
#     path("map/", views.displacement_map, name="displacement_map"),
#     path("geojson/", views.displacement_geojson, name="displacement_geojson"),
#     path("add/", views.add_displacement_event, name="add_displacement_event"),
#     path("upload-csv/", views.upload_displacement_csv, name="upload_displacement_csv"),
#     path(
#         "upload_political_violence/",
#         views.upload_political_violence,
#         name="upload_political_violence",
#     ),
#     path(
#         "add_political_violence/",
#         views.add_political_violence_record,
#         name="add_political_violence_record",
#     ),
#     path(
#         "fatalities/province/<int:province_id>/",
#         views.fatalities_timeseries,
#         name="fatalities_timeseries",
#     ),
#     path(
#         "timeseries/province/<int:province_id>/",
#         views.violence_timeseries,
#         name="violence_timeseries",
#     ),
#     path(
#         "geojson/fatalities/",
#         views.fatalities_choropleth_geojson,
#         name="fatalities_choropleth_geojson",
#     ),
#     path(
#         "map/fatalities/",
#         views.fatalities_choropleth_map,
#         name="fatalities_choropleth_map",
#     ),
#     path("api/choropleth/", views.political_violence_choropleth, name="choropleth_api"),
# ]
