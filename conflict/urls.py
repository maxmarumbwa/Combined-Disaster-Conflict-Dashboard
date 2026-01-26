from django.urls import path
from . import views

urlpatterns = [
    # API-based political violence URLs
    path("api/geojson/", views.political_violence_choropleth, name="choropleth_api"),
    path(
        "upload_political_violence/",
        views.upload_political_violence,
        name="upload_political_violence",
    ),
    path(
        "map/choropleth/",
        views.political_violence_choropleth_page,
        name="political_violence_choropleth",
    ),
    path(
        "api/political_violence/yearly_anomaly/",
        views.yearly_political_violence_anom_api,
        name="yearly_political_violence_anom_api",
    ),
    path(
        "api/analytics/",
        views.political_violence_table_api,
        name="political_violence_table_api",
    ),
    # Tables and Charts
    # path(
    #     "table/",
    #     views.political_violence_table,
    #     name="political_violence_table",
    # ),
    path(
        "api/table/",
        views.political_violence_table_paginated_api,
        name="political_violence_table_api",
    ),
    path(
        "api/geojson/political_violence/yearly_anomaly/",
        views.adm1_yearly_violence_geojson,
        name="adm1_yearly_violence_geojson",
    ),
    path(
        "derived/geojson_political_conflict_yearly_anomaly/",
        views.geojson_political_conflict_yearly_anomaly,
        name="geojson_political_conflict_yearly_anomaly",
    ),
    path(
        "table/political_violence/",
        views.political_conflict_table,
        name="political_conflict_table",
    ),
    path(
        "chart/political_violence/",
        views.political_conflict_chart,
        name="political_conflict_chart",
    ),
    path(
        "pie_chart/political_violence/",
        views.political_conflict_pie_chart,
        name="yearly piechart political violence",
    ),
    path(
        "derived/yearly_political_violence/",
        views.yearly_political_violence_api,
        name="year_political_violence",
    ),
    path(
        "derived/political_conflict_monthly_anomaly/",
        views.political_conflict_monthly_anomaly,
        name="political_conflict_monthly_anomaly",
    ),
    path(
        "api/political_violence/monthly_anomaly/",
        views.monthly_political_violence_anom_api,
        name="monthly_political_violence_anom_api",
    ),
    path(
        "derived/political_conflict_yearly_anomaly/",
        views.political_conflict_yearly_anomaly,
        name="political_conflict_yearly_anomaly",
    ),
]

# ==================================================================================================

#                                         OLD CODE

# ==================================================================================================


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
