from django.shortcuts import render
from djgeojson.views import GeoJSONLayerView
from .models import DisplacementEvent


# 1️⃣ View to render the HTML map page
def displacement_map(request):
    return render(request, "displacements_map.html")


# 2️⃣ View to serve displacement data as GeoJSON
class DisplacementGeoJSON(GeoJSONLayerView):
    model = DisplacementEvent
    geometry_field = "location"
    properties = (
        "external_id",
        "displacement_type",
        "displacement_name",
        "figure",
        "displacement_date",
    )
