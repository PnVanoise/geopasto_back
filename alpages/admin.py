from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Logement, QuartierUP, Commodite, LogementCommodite
from .models import UnitePastorale, ProprietaireFoncier, QuartierPasto, UPProprietaire
from .models import TypeConvention, ConventionDExploitation, Eleveur, Exploitant, EtreCompose, SubventionPNV, AbriDUrgence, BeneficierDe
from .models import SituationDExploitation, Exploiter
from .models import TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan
from .models import Ruche, Berger, TypeCheptel, GardeSituation, Elever
from .models import TypeEvenement, Evenement

from .models import LogementTest

admin.site.register(Logement, LeafletGeoAdmin)
admin.site.register(QuartierUP, LeafletGeoAdmin)
admin.site.register(Commodite, LeafletGeoAdmin)
admin.site.register(LogementCommodite, LeafletGeoAdmin)

# Administratif
admin.site.register(UnitePastorale, LeafletGeoAdmin)
admin.site.register(ProprietaireFoncier, LeafletGeoAdmin)
admin.site.register(QuartierPasto, LeafletGeoAdmin)
admin.site.register(UPProprietaire, LeafletGeoAdmin)

admin.site.register(TypeConvention, LeafletGeoAdmin)
admin.site.register(ConventionDExploitation, LeafletGeoAdmin)
admin.site.register(SituationDExploitation, LeafletGeoAdmin)
admin.site.register(Exploiter, LeafletGeoAdmin)
admin.site.register(Eleveur, LeafletGeoAdmin)
admin.site.register(Exploitant, LeafletGeoAdmin)
admin.site.register(EtreCompose, LeafletGeoAdmin)
admin.site.register(SubventionPNV, LeafletGeoAdmin)
admin.site.register(AbriDUrgence, LeafletGeoAdmin)
admin.site.register(BeneficierDe, LeafletGeoAdmin)

# Ruche / Berger / TypeCheptel
admin.site.register(Ruche, LeafletGeoAdmin)
admin.site.register(Berger, LeafletGeoAdmin)
admin.site.register(TypeCheptel, LeafletGeoAdmin)
admin.site.register(GardeSituation, LeafletGeoAdmin)
admin.site.register(Elever, LeafletGeoAdmin)

# Evenements
admin.site.register(TypeEvenement, LeafletGeoAdmin)
admin.site.register(Evenement, LeafletGeoAdmin)

# Bloc plans de suivi (bleu)
admin.site.register(TypeDeSuivi, LeafletGeoAdmin)
admin.site.register(PlanDeSuivi, LeafletGeoAdmin)
admin.site.register(TypeDeMesure, LeafletGeoAdmin)
admin.site.register(MesureDePlan, LeafletGeoAdmin)

# TEST CC
admin.site.register(LogementTest, LeafletGeoAdmin)
