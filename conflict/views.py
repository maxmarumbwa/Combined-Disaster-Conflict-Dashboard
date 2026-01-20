from django.http import JsonResponse
from django.shortcuts import render
from .models import DisplacementEvent


def displacement_map(request):
    return render(request, "displacement_map.html")


from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from .models import DisplacementEvent


def displacement_geojson(request):
    features = []

    for event in DisplacementEvent.objects.all():
        geom = GEOSGeometry(event.location.geojson)  # convert string → geometry dict

        features.append(
            {
                "type": "Feature",
                "geometry": geom.json,  # this is a dict, not a string
                "properties": {
                    "id": event.external_id,
                    "type": event.displacement_type,
                    "name": event.displacement_name,
                    "figure": event.figure,
                    "date": str(event.displacement_date),
                },
            }
        )
    return JsonResponse({"type": "FeatureCollection", "features": features})


from django.shortcuts import render, redirect
from .forms import DisplacementEventForm


def add_displacement_event(request):
    if request.method == "POST":
        form = DisplacementEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("displacement_map")  # Redirect to map after saving
    else:
        form = DisplacementEventForm()

    return render(request, "add_displacement_event.html", {"form": form})
