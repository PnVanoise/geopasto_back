from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import QuartierUP

alpages_mapping = {
    "quartier_code": "code_quart",
    "surface": "surface",
    "up_code": "Field_1",
    "up_nom_1": "NOM_UP",
    "up_nom_2": "NOM_2",
    "quartier_code_court": "Quartier",
    "quartier_nom": "Nom_quart",
    "geom": "MULTIPOLYGON",
}

alpages_shp = Path(__file__).resolve().parent / "data" / "quartiers_alpages.shp"


def run(verbose=True):
    lm = LayerMapping(QuartierUP, alpages_shp, alpages_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

