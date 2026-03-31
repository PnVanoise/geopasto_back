from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from alpages.views import LogementViewset, get_choices_logement, CommoditeViewset, LogementCommoditeViewset
from alpages.views import UnitePastoraleViewset, ProprietaireFoncierViewset, QuartierPastoViewset, ProprietaireUnitePastoraleViewset
from alpages.views import TypeConventionViewset, ConventionDExploitationViewset, EleveurViewset, TypeDExploitantViewset, ExploitantViewset
from alpages.views import SituationDExploitationViewset, ExploiterViewset
from alpages.views import TypeDeSuiviViewset, PlanDeSuiviViewset, TypeDeMesureViewset, MesureDePlanViewset, EtreComposeViewset, SubventionPNVViewset, AbriDUrgenceViewset, AbriDUrgenceCommoditeViewset, BeneficierDeViewset

from alpages.views import RucheViewset, BergerViewset, TypeCheptelViewset, GardeSituationViewset
from alpages.views import TypeEvenementViewset, EvenementViewset

from alpages.views import TypeEquipementViewset, EquipementExploitantViewset, EquipementAlpageViewset

##########
# Refactoring Elever et TypeCheptel pour les fusionner en Cheptel et Type_cheptel
# dlg le 10/2/26
from alpages.views import CheptelViewset, Type_cheptelViewset, ProductionViewset, Categorie_pensionViewset, EspeceViewset, RaceViewset, Categorie_animauxViewset
##########

router = routers.SimpleRouter()


router.register('logement', LogementViewset, basename='logement')
router.register('commodite', CommoditeViewset, basename='commodite')
router.register('logementCommodite', LogementCommoditeViewset, basename='logementcommodite')

router.register('abriDUrgenceCommodite', AbriDUrgenceCommoditeViewset, basename='abridurgencecommodite')

# Bloc administratif
router.register('unitePastorale', UnitePastoraleViewset, basename='unitepastorale')
router.register('proprietaireFoncier', ProprietaireFoncierViewset, basename='proprietairefoncier')
router.register('quartierPasto', QuartierPastoViewset, basename='quartierpasto')
router.register('proprietaireUP', ProprietaireUnitePastoraleViewset, basename='proprietaireunitepastorale')

router.register('typeConvention', TypeConventionViewset, basename='typeconvention')
router.register('conventionExploitation', ConventionDExploitationViewset, basename='conventionexploitation')
router.register('situationExploitation', SituationDExploitationViewset, basename='situationexploitation')
router.register('exploiter', ExploiterViewset, basename='exploiter')

router.register('eleveur', EleveurViewset, basename='eleveur')


router.register('typeExploitant', TypeDExploitantViewset, basename='typeexploitant')
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

# Evenements
router.register('typeEvenement', TypeEvenementViewset, basename='typeevenement')
router.register('evenement', EvenementViewset, basename='evenement')

# BLoc bleu
router.register('typeSuivi', TypeDeSuiviViewset, basename='typesuivi')
router.register('planSuivi', PlanDeSuiviViewset, basename='plansuivi')
router.register('typeMesure', TypeDeMesureViewset, basename='typemesure')
router.register('mesurePlan', MesureDePlanViewset, basename='mesureplan')

router.register('typeEquipement', TypeEquipementViewset, basename='typeequipement')
router.register('equipementAlpage', EquipementAlpageViewset, basename='equipementalpage')
router.register('equipementExploitant', EquipementExploitantViewset, basename='equipementexploitant')

###########
# Refactoring Elever et TypeCheptel pour les fusionner en Cheptel et Type_cheptel
# dlg le 10/2/26
router.register('cheptel', CheptelViewset, basename='cheptel')
router.register('type_cheptel', Type_cheptelViewset, basename='type_cheptel')
router.register('production', ProductionViewset, basename='production')
router.register('categorie_pension', Categorie_pensionViewset, basename='categorie_pension')
router.register('espece', EspeceViewset, basename='espece')
router.register('race', RaceViewset, basename='race')
router.register('categorie_animaux', Categorie_animauxViewset, basename='categorie_animaux')
###########


urlpatterns = [
    path('admin/', admin.site.urls),
    path('choices_logement/', get_choices_logement, name='get_choices_logement'),
    path('api/', include(router.urls)),
    path('', include('accounts.urls')),
]
