import csv
from io import TextIOWrapper
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.gis.geos import Point
from .models import DisplacementEvent
from .forms import DisplacementEventForm
from .forms import CSVUploadForm


# Map view
def displacement_map(request):
    return render(request, "displacement_map.html")


# GeoJSON endpoint
def displacement_geojson(request):
    features = []

    for event in DisplacementEvent.objects.all():
        features.append(
            {
                "type": "Feature",
                "geometry": event.location.json,  # already GeoJSON
                "properties": {
                    "id": event.external_id,
                    "type": event.displacement_type,
                    "name": event.displacement_name,
                    "figure": event.figure,
                    "date": event.displacement_date.isoformat(),
                },
            }
        )

    return JsonResponse({"type": "FeatureCollection", "features": features}, safe=False)


# Add form


def add_displacement_event(request):
    if request.method == "POST":
        form = DisplacementEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Displacement event added successfully.")
            return redirect("displacement_map")
    else:
        form = DisplacementEventForm()

    return render(request, "add_displacement_event.html", {"form": form})


######  Upload from csv


def upload_displacement_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")

            reader = csv.DictReader(csv_file)
            created, skipped = 0, 0

            for row in reader:
                try:
                    DisplacementEvent.objects.update_or_create(
                        external_id=int(row["external_id"]),
                        defaults={
                            "displacement_type": row["displacement_type"],
                            "displacement_name": row.get("displacement_name", ""),
                            "figure": int(row["figure"]),
                            "displacement_date": datetime.strptime(
                                row["displacement_date"], "%Y-%m-%d"
                            ).date(),
                            "location": Point(
                                float(row["longitude"]),
                                float(row["latitude"]),
                                srid=4326,
                            ),
                        },
                    )
                    created += 1
                except Exception:
                    skipped += 1

            messages.success(
                request,
                f"CSV upload complete: {created} records saved, {skipped} skipped.",
            )
            return redirect("displacement_map")
    else:
        form = CSVUploadForm()

    return render(request, "upload_displacement_csv.html", {"form": form})
