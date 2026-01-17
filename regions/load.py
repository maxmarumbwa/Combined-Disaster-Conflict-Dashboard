from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import adm1

adm1_mapping = {
    "shapename": "shapeName",
    "shapeiso": "shapeISO",
    "shapeid": "shapeID",
    "shapegroup": "shapeGroup",
    "shapetype": "shapeType",
    "geom": "geometry",
}

# Go to the project root, then static/geojson
adm1_shp = (
    Path(__file__).resolve().parent.parent  # move up from regions → project root
    / "static"
    / "geojson"
    / "geoBoundaries-COD-ADM1.geojson"
)


def run(verbose=True):
    lm = LayerMapping(adm1, adm1_shp, adm1_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
