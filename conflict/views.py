import json
import csv
from io import TextIOWrapper
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.gis.geos import Point
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DisplacementEvent
from .forms import DisplacementEventForm
from .forms import CSVUploadForm
from conflict.models import PoliticalViolenceAdm1Monthly
from regions.models import adm1
from .forms import PoliticalViolenceUploadForm, PoliticalViolenceManualForm

# Upload political violence data from CSV


def upload_political_violence(request):
    if request.method == "POST":
        form = PoliticalViolenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]
            reset_table = form.cleaned_data["reset"]

            if reset_table:
                PoliticalViolenceAdm1Monthly.objects.all().delete()
                messages.warning(request, "Deleted all existing records.")

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = list(csv.DictReader(decoded_file))
            total_rows = len(reader)

            request.session["import_progress"] = 0

            imported_rows = 0
            skipped_rows = 0
            province_totals = {}

            for index, row in enumerate(reader, start=1):
                # Update progress in session
                request.session["import_progress"] = int(index / total_rows * 100)
                request.session.modified = True

                province_name = row.get("\ufeffProvince") or row.get("Province")
                province_name = province_name.strip() if province_name else None
                month_str = row["Month"].strip()
                year = int(row["Year"].strip())
                events = int(row["Events"].strip())
                fatalities = int(row["Fatalities"].strip())

                if not province_name:
                    skipped_rows += 1
                    continue

                try:
                    province_obj = adm1.objects.get(shapename2__iexact=province_name)
                except adm1.DoesNotExist:
                    skipped_rows += 1
                    continue

                month_number = {
                    "January": 1,
                    "February": 2,
                    "March": 3,
                    "April": 4,
                    "May": 5,
                    "June": 6,
                    "July": 7,
                    "August": 8,
                    "September": 9,
                    "October": 10,
                    "November": 11,
                    "December": 12,
                }.get(month_str, 0)

                if month_number == 0:
                    skipped_rows += 1
                    continue

                # Prevent duplication
                obj, created = PoliticalViolenceAdm1Monthly.objects.get_or_create(
                    province=province_obj,
                    month=month_number,
                    year=year,
                    defaults={"events": events, "fatalities": fatalities},
                )
                if not created:
                    obj.events = events
                    obj.fatalities = fatalities
                    obj.save()

                imported_rows += 1
                province_totals[province_name] = (
                    province_totals.get(province_name, 0) + 1
                )

            messages.success(
                request,
                f"Imported {imported_rows} of {total_rows} rows. Skipped {skipped_rows}.",
            )
            messages.info(
                request,
                "Rows per province: "
                + ", ".join([f"{k}: {v}" for k, v in province_totals.items()]),
            )

            # Reset progress
            request.session["import_progress"] = 100
            return render(request, "conflict/upload_result.html")

    else:
        form = PoliticalViolenceUploadForm()

    return render(request, "conflict/upload.html", {"form": form})


# API for getting geojson data from admin1 monthly political violence data


@api_view(["GET"])
def political_violence_choropleth(request):
    """
    Returns monthly events/fatalities per province for choropleth.
    Optional GET parameters:
        - year
        - month
        - indicator: "events" or "fatalities"
    """
    year = request.GET.get("year")
    month = request.GET.get("month")
    indicator = request.GET.get("indicator", "fatalities")  # default

    # Filter by year/month if provided
    qs = PoliticalViolenceAdm1Monthly.objects.all()
    if year:
        qs = qs.filter(year=year)
    if month:
        qs = qs.filter(month=month)

    # Build a lookup: province_id -> value
    value_lookup = {row.province.id: getattr(row, indicator, 0) for row in qs}

    # Build GeoJSON
    features = []
    for province in adm1.objects.all():
        geojson_geom = json.loads(province.geom.geojson)
        features.append(
            {
                "type": "Feature",
                "geometry": geojson_geom,
                "properties": {
                    "name": province.shapename2,
                    "value": value_lookup.get(province.id, 0),  # monthly value
                },
            }
        )

    return Response({"type": "FeatureCollection", "features": features})


# View to render the choropleth page with filters
def political_violence_choropleth_page(request):
    # Distinct years from database
    years = (
        PoliticalViolenceAdm1Monthly.objects.values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )

    # Month choices (value, label)
    months = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    ]

    # Indicators
    indicators = [
        ("fatalities", "Fatalities"),
        ("events", "Events"),
    ]

    context = {
        "years": years,
        "months": months,
        "indicators": indicators,
    }

    return render(
        request,
        # "conflict/api_based/api_fatalities_choropleth.html",
        "conflict/api_based/test.html",
        context,
    )


# # View to render a table of political violence data with optional year/month filters
# from conflict.models import PoliticalViolenceAdm1Monthly
# def political_violence_table(request):
#     year = request.GET.get("year")
#     month = request.GET.get("month")
#     qs = PoliticalViolenceAdm1Monthly.objects.select_related("province")

#     if year:
#         qs = qs.filter(year=year)
#     if month:
#         qs = qs.filter(month=month)

#     qs = qs.order_by("province__shapename2", "year", "month")

#     context = {
#         "records": qs,
#     }

#     return render(
#         request,
#         "conflict/api_based/political_violence_table.html",
#         context,
#     )


# Table API view for political violence data with pagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from conflict.models import PoliticalViolenceAdm1Monthly
from .serializers import PoliticalViolenceAdm1MonthlySerializer
from .pagination import StandardResultsSetPagination


@api_view(["GET"])
def political_violence_table_api(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    province_id = request.GET.get("province")

    qs = PoliticalViolenceAdm1Monthly.objects.select_related("province")

    if year:
        qs = qs.filter(year=year)

    if month:
        qs = qs.filter(month=month)

    if province_id:
        qs = qs.filter(province_id=province_id)

    qs = qs.order_by("province__shapename2", "year", "month")

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(qs, request)

    serializer = PoliticalViolenceAdm1MonthlySerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


def political_conflict_table(request):
    return render(request, "conflict/api_based/political_violence_table.html")


def political_conflict_chart(request):
    return render(request, "conflict/api_based/political_violence_chart.html")


# =========================================================================================================
# 				                                 OLD
# =========================================================================================================


# import csv
# from io import TextIOWrapper
# from datetime import datetime
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.gis.geos import Point
# from .models import DisplacementEvent
# from .forms import DisplacementEventForm
# from .forms import CSVUploadForm
# from conflict.models import PoliticalViolenceAdm1Monthly
# from regions.models import adm1
# from .forms import PoliticalViolenceUploadForm, PoliticalViolenceManualForm


# # Map view
# def displacement_map(request):
#     return render(request, "displacement_map.html")


# # GeoJSON endpoint
# def displacement_geojson(request):
#     features = []

#     for event in DisplacementEvent.objects.all():
#         features.append(
#             {
#                 "type": "Feature",
#                 "geometry": event.location.json,  # already GeoJSON
#                 "properties": {
#                     "id": event.external_id,
#                     "type": event.displacement_type,
#                     "name": event.displacement_name,
#                     "figure": event.figure,
#                     "date": event.displacement_date.isoformat(),
#                 },
#             }
#         )

#     return JsonResponse({"type": "FeatureCollection", "features": features}, safe=False)


# # Add form


# def add_displacement_event(request):
#     if request.method == "POST":
#         form = DisplacementEventForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Displacement event added successfully.")
#             return redirect("displacement_map")
#     else:
#         form = DisplacementEventForm()

#     return render(request, "add_displacement_event.html", {"form": form})


# ######  Upload from csv


# def upload_displacement_csv(request):
#     if request.method == "POST":
#         form = CSVUploadForm(request.POST, request.FILES)

#         if form.is_valid():
#             csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")

#             reader = csv.DictReader(csv_file)
#             created, skipped = 0, 0

#             for row in reader:
#                 try:
#                     DisplacementEvent.objects.update_or_create(
#                         external_id=int(row["external_id"]),
#                         defaults={
#                             "displacement_type": row["displacement_type"],
#                             "displacement_name": row.get("displacement_name", ""),
#                             "figure": int(row["figure"]),
#                             "displacement_date": datetime.strptime(
#                                 row["displacement_date"], "%Y-%m-%d"
#                             ).date(),
#                             "location": Point(
#                                 float(row["longitude"]),
#                                 float(row["latitude"]),
#                                 srid=4326,
#                             ),
#                         },
#                     )
#                     created += 1
#                 except Exception:
#                     skipped += 1

#             messages.success(
#                 request,
#                 f"CSV upload complete: {created} records saved, {skipped} skipped.",
#             )
#             return redirect("displacement_map")
#     else:
#         form = CSVUploadForm()

#     return render(request, "upload_displacement_csv.html", {"form": form})


# # Manual data entry for political violence
# def add_political_violence_record(request):
#     if request.method == "POST":
#         form = PoliticalViolenceManualForm(request.POST)

#         if form.is_valid():
#             province = form.cleaned_data["province"]
#             month = int(form.cleaned_data["month"])
#             year = form.cleaned_data["year"]
#             events = form.cleaned_data["events"]
#             fatalities = form.cleaned_data["fatalities"]

#             obj, created = PoliticalViolenceAdm1Monthly.objects.get_or_create(
#                 province=province,
#                 month=month,
#                 year=year,
#                 defaults={"events": events, "fatalities": fatalities},
#             )

#             if not created:
#                 obj.events = events
#                 obj.fatalities = fatalities
#                 obj.save()
#                 messages.info(request, "Existing record updated.")
#             else:
#                 messages.success(request, "New record added successfully.")

#             return redirect("add_political_violence_record")

#     else:
#         form = PoliticalViolenceManualForm()

#     return render(request, "conflict/add_manual.html", {"form": form})


# # Chart view for based on province id
# # conflict/views.py
# from django.shortcuts import render, get_object_or_404
# from conflict.models import PoliticalViolenceAdm1Monthly
# from regions.models import adm1


# def fatalities_timeseries(request, province_id):
#     province = get_object_or_404(adm1, id=province_id)

#     qs = (
#         PoliticalViolenceAdm1Monthly.objects.filter(province=province)
#         .order_by("year", "month")
#         .values("year", "month", "fatalities")
#     )

#     labels = [f"{r['year']}-{str(r['month']).zfill(2)}" for r in qs]
#     data = [r["fatalities"] for r in qs]

#     context = {
#         "province": province,
#         "labels": labels,
#         "data": data,
#     }
#     return render(request, "conflict/fatalities_timeseries.html", context)


# # Chart view for fatalities time series
# # conflict/views.py
# from django.shortcuts import render, get_object_or_404
# from conflict.models import PoliticalViolenceAdm1Monthly
# from regions.models import adm1


# def violence_timeseries(request, province_id):
#     metric = request.GET.get("metric", "fatalities")  # default
#     if metric not in ["fatalities", "events"]:
#         metric = "fatalities"

#     province = get_object_or_404(adm1, id=province_id)

#     qs = (
#         PoliticalViolenceAdm1Monthly.objects.filter(province=province)
#         .order_by("year", "month")
#         .values("year", "month", metric)
#     )

#     labels = [f"{r['year']}-{str(r['month']).zfill(2)}" for r in qs]
#     data = [r[metric] for r in qs]

#     context = {
#         "province": province,
#         "labels": labels,
#         "data": data,
#         "metric": metric,
#     }
#     return render(request, "conflict/violence_timeseries.html", context)


# # GeoJSON with fatalities for choropleth
# # conflict/views.py
# from django.http import HttpResponse
# from django.core.serializers import serialize
# from regions.models import adm1
# from conflict.models import PoliticalViolenceAdm1Monthly
# import json


# def fatalities_choropleth_geojson(request):
#     year = 2023
#     month = 1

#     provinces = adm1.objects.all()

#     # attach fatalities dynamically
#     features = []
#     for province in provinces:
#         record = PoliticalViolenceAdm1Monthly.objects.filter(
#             province=province, year=year, month=month
#         ).first()

#         fatalities = record.fatalities if record else 0

#         features.append({"id": province.id, "fatalities": fatalities})

#     geojson = json.loads(
#         serialize("geojson", provinces, geometry_field="geom", fields=("shapename",))
#     )

#     # inject fatalities into properties
#     for feature in geojson["features"]:
#         pid = feature["id"]
#         match = next((f for f in features if f["id"] == pid), None)
#         feature["properties"]["fatalities"] = match["fatalities"] if match else 0

#     return HttpResponse(json.dumps(geojson), content_type="application/json")


# # Create a view to render the choropleth page
# def fatalities_choropleth_map(request):
#     return render(request, "conflict/fatalities_choropleth.html")


# # select year and month  and variable to display for choropleth
# import json
# from django.shortcuts import render
# from django.db.models import Sum
# from regions.models import adm1
# from conflict.models import PoliticalViolenceAdm1Monthly


# ## Plot choropleth map with year/month filter
# def fatalities_choropleth_map(request):
#     """
#     Choropleth map showing fatalities or events per province with optional year/month filter.
#     """
#     # Get GET parameters
#     year = request.GET.get("year")
#     month = request.GET.get("month")
#     indicator = request.GET.get("indicator", "fatalities")  # default to fatalities

#     # Prepare dropdown options
#     years = (
#         PoliticalViolenceAdm1Monthly.objects.values_list("year", flat=True)
#         .distinct()
#         .order_by("year")
#     )
#     months = range(1, 13)
#     indicators = ["fatalities", "events"]

#     features = []

#     if year and month:
#         # Aggregate based on selected indicator
#         qs = (
#             PoliticalViolenceAdm1Monthly.objects.filter(year=year, month=month)
#             .values("province")
#             .annotate(total_value=Sum(indicator))
#         )

#         value_lookup = {row["province"]: row["total_value"] for row in qs}

#         for province in adm1.objects.all():
#             geojson_geom = json.loads(province.geom.geojson)

#             features.append(
#                 {
#                     "type": "Feature",
#                     "geometry": geojson_geom,
#                     "properties": {
#                         "name": province.shapename2,
#                         "value": value_lookup.get(
#                             province.id, 0
#                         ),  # store as generic 'value'
#                     },
#                 }
#             )

#     context = {
#         "years": years,
#         "months": months,
#         "indicators": indicators,
#         "selected_year": year,
#         "selected_month": month,
#         "selected_indicator": indicator,
#         "geojson": {"type": "FeatureCollection", "features": features},
#     }

#     return render(request, "conflict/fatalities_choropleth.html", context)


# # GENERIC API VIEW FOR TABLE ,CHOROPLETH DATA

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from regions.models import adm1
# from conflict.models import PoliticalViolenceAdm1Monthly
# import json


# @api_view(["GET"])
# def political_violence_choropleth(request):
#     """
#     Returns monthly events/fatalities per province for choropleth.
#     Optional GET parameters:
#         - year
#         - month
#         - indicator: "events" or "fatalities"
#     """
#     year = request.GET.get("year")
#     month = request.GET.get("month")
#     indicator = request.GET.get("indicator", "fatalities")  # default

#     # Filter by year/month if provided
#     qs = PoliticalViolenceAdm1Monthly.objects.all()
#     if year:
#         qs = qs.filter(year=year)
#     if month:
#         qs = qs.filter(month=month)

#     # Build a lookup: province_id -> value
#     value_lookup = {row.province.id: getattr(row, indicator, 0) for row in qs}

#     # Build GeoJSON
#     features = []
#     for province in adm1.objects.all():
#         geojson_geom = json.loads(province.geom.geojson)
#         features.append(
#             {
#                 "type": "Feature",
#                 "geometry": geojson_geom,
#                 "properties": {
#                     "name": province.shapename2,
#                     "value": value_lookup.get(province.id, 0),  # monthly value
#                 },
#             }
#         )

#     return Response({"type": "FeatureCollection", "features": features})
