from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import UnitePastorale

ups_mapping = {
    "id_unite_pastorale": "id_unite_p",
    "code_up": "code_UP",
    "nom_up": "nom_UP",
    "annee_version": "annee_vers",
    "version_active": "version_ac",
    "geometry": "MULTIPOLYGON",
}

ups_shp = Path(__file__).resolve().parent / "data" / "UP_coeur_fields_OK.shp"


def run(verbose=True):
    lm = LayerMapping(UnitePastorale, ups_shp, ups_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

