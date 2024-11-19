from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import QuartierPasto

quartiers_mapping = {
    "id_quartier": "id",
    "code_quartier": "code",
    "nom_quartier": "nom",
    "geometry": "POLYGON",
}

# quartiers_shp = Path(__file__).resolve().parent / "data" / "quartiers_pierre_brune_raw.shp"
quartiers_shp = Path(__file__).resolve().parent / "data" / "quartiers_loza.shp"


def run(verbose=True):
    lm = LayerMapping(QuartierPasto, quartiers_shp, quartiers_mapping, transform=True)
    lm.save(strict=True, verbose=verbose)

