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
from conflict.models import PoliticalViolenceAdm1Monthly
from regions.models import adm1
from .forms import PoliticalViolenceUploadForm


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

            # Read CSV
            total_rows = 0
            imported_rows = 0
            skipped_rows = 0
            province_totals = {}

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                total_rows += 1

                # Handle BOM
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

                # Prevent duplication using get_or_create
                obj, created = PoliticalViolenceAdm1Monthly.objects.get_or_create(
                    province=province_obj,
                    month=month_number,
                    year=year,
                    defaults={"events": events, "fatalities": fatalities},
                )
                if not created:
                    # Optionally update values if needed
                    obj.events = events
                    obj.fatalities = fatalities
                    obj.save()

                imported_rows += 1
                province_totals[province_name] = (
                    province_totals.get(province_name, 0) + 1
                )

            messages.success(
                request,
                f"Processed {total_rows} rows. Imported {imported_rows}, Skipped {skipped_rows}",
            )
            messages.info(
                request,
                "Rows per province: "
                + ", ".join([f"{k}: {v}" for k, v in province_totals.items()]),
            )

            return render(request, "conflict/upload_result.html")

    else:
        form = PoliticalViolenceUploadForm()

    return render(request, "conflict/upload.html", {"form": form})
