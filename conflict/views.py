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
