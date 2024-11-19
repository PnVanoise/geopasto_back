from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from alpages.views import LogementViewset, QuartierUPViewset, QuartieralpageViewset, get_choices_logement, CommoditeViewset, LogementCommoditeViewset
from alpages.views import UnitePastoraleViewset, ProprietaireFoncierViewset, QuartierPastoViewset, UPProprietaireViewset
from alpages.views import TypeConventionViewset, ConventionDExploitationViewset, EleveurViewset, ExploitantViewset
from alpages.views import SituationDExploitationViewset, ExploiterViewset
from alpages.views import TypeDeSuiviViewset, PlanDeSuiviViewset, TypeDeMesureViewset, MesureDePlanViewset, EtreComposeViewset, SubventionPNVViewset, AbriDUrgenceViewset, BeneficierDeViewset

from alpages.views import RucheViewset, BergerViewset, TypeCheptelViewset, GardeSituationViewset, EleverViewset
from alpages.views import TypeEvenementViewset, EvenementViewset

from alpages.views import LogementTestViewset

router = routers.SimpleRouter()
router.register('logement', LogementViewset, basename='logement')
router.register('commodite', CommoditeViewset, basename='commodite')
router.register('logementCommodite', LogementCommoditeViewset, basename='logementcommodite')
router.register('quartierUP', QuartierUPViewset, basename='quartierup')
router.register('quartierAlpage', QuartieralpageViewset, basename='quartieralpage')

# Bloc administratif
router.register('unitePastorale', UnitePastoraleViewset, basename='unitepastorale')
router.register('proprietaireFoncier', ProprietaireFoncierViewset, basename='proprietairefoncier')
router.register('quartierPasto', QuartierPastoViewset, basename='quartierpasto')
router.register('upproprietaire', UPProprietaireViewset, basename='upproprietaire')

router.register('typeConvention', TypeConventionViewset, basename='typeconvention')
router.register('conventionExploitation', ConventionDExploitationViewset, basename='conventionexploitation')
router.register('situationExploitation', SituationDExploitationViewset, basename='situationexploitation')
router.register('exploiter', ExploiterViewset, basename='exploiter')

router.register('eleveur', EleveurViewset, basename='eleveur')
router.register('exploitant', ExploitantViewset, basename='exploitant')
router.register('etreCompose', EtreComposeViewset, basename='etrecompose')
router.register('subventionPNV', SubventionPNVViewset, basename='subventionpnv')
router.register('abriDUrgence', AbriDUrgenceViewset, basename='abridurgence')
router.register('beneficierDe', BeneficierDeViewset, basename='beneficierde')

# Ruche / Berger / TypeCheptel
router.register('ruche', RucheViewset, basename='ruche')
router.register('berger', BergerViewset, basename='berger')
router.register('typeCheptel', TypeCheptelViewset, basename='typecheptel')
router.register('gardeSituation', GardeSituationViewset, basename='gardesituation')
router.register('elever', EleverViewset, basename='elever')

# Evenements
router.register('typeEvenement', TypeEvenementViewset, basename='typeevenement')
router.register('evenement', EvenementViewset, basename='evenement')

# BLoc bleu
router.register('typeSuivi', TypeDeSuiviViewset, basename='typesuivi')
router.register('planSuivi', PlanDeSuiviViewset, basename='plansuivi')
router.register('typeMesure', TypeDeMesureViewset, basename='typemesure')
router.register('mesurePlan', MesureDePlanViewset, basename='mesureplan')

# TEST CC
router.register('logementTest', LogementTestViewset, basename='logementtest')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('choices_logement/', get_choices_logement, name='get_choices_logement'),
    path('api/', include(router.urls)),
]
