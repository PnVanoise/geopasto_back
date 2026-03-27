import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from alpages.viewsets_base import BaseModelViewSet
from rest_framework.decorators import api_view, action

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType

from alpages.models import Logement, QuartierUP, Quartieralpage, Commodite, LogementCommodite
from alpages.models import UnitePastorale, ProprietaireFoncier, QuartierPasto, UPProprietaire
from alpages.models import TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan
from alpages.models import TypeConvention, ConventionDExploitation, Eleveur, TypeDExploitant, Exploitant, EtreCompose, SubventionPNV, AbriDUrgence, AbriDUrgenceCommodite, BeneficierDe
from alpages.models import SituationDExploitation, Exploiter

from alpages.models import Cheptel, Type_cheptel, Production, Categorie_pension, Espece, Race, Categorie_animaux
from alpages.serializers import CheptelSerializer, Type_cheptelSerializer, ProductionSerializer, Categorie_pensionSerializer, EspeceSerializer, RaceSerializer, Categorie_animauxSerializer

from alpages.models import Ruche, Berger, TypeCheptel, GardeSituation, Elever
from alpages.serializers import RucheSerializer, BergerSerializer, TypeCheptelSerializer, GardeSituationSerializer, EleverSerializer

from alpages.models import TypeEvenement, Evenement
from alpages.serializers import TypeEvenementSerializer, EvenementSerializer

from alpages.serializers import LogementSerializer, QuartierUPSerializer, QuartieralpageSerializer, CommoditeSerializer, LogementCommoditeSerializer
from alpages.serializers import UnitePastoraleSerializer, UnitePastoraleLSerializer, ProprietaireFoncierSerializer, QuartierPastoSerializer, UPProprietaireSerializer
from alpages.serializers import TypeDeSuiviSerializer, PlanDeSuiviSerializer, TypeDeMesureSerializer, MesureDePlanSerializer
from alpages.serializers import TypeConventionSerializer, ConventionDExploitationSerializer, EleveurSerializer, TypeDExploitantSerializer, ExploitantSerializer, EtreComposeSerializer, SubventionPNVSerializer, AbriDUrgenceSerializer, AbriDUrgenceCommoditeSerializer, BeneficierDeSerializer
from alpages.serializers import SituationDExploitationSerializer, ExploiterSerializer

from alpages.models import TypeEquipement, EquipementExploitant, EquipementAlpage
from alpages.serializers import TypeEquipementSerializer, EquipementExploitantSerializer, EquipementAlpageSerializer

##########
# Refactoring Elever et TypeCheptel pour les fusionner en Cheptel et Type_cheptel
# dlg le 10/2/26
from alpages.models import Cheptel, Type_cheptel, Production, Categorie_pension, Espece, Race, Categorie_animaux
from alpages.serializers import CheptelSerializer, Type_cheptelSerializer, ProductionSerializer, Categorie_pensionSerializer, EspeceSerializer, RaceSerializer, Categorie_animauxSerializer
##########

from .choices_logement import LST_STATUT, LST_ACCES_FINAL, LST_PROPRIETE, LST_TYPE_LOGEMENT, LST_MULTIUSAGE, LST_ACCUEIL_PUBLIC,\
                              LST_ACTIVITE_LAITIERE, LST_ETAT_BATIMENT, LST_SURFACE_LOGEMENT, LST_WC, LST_ALIM_ELECTRIQUE, LST_ALIM_EAU,\
                              LST_ORIGINE_EAU, LST_QUALITE_EAU, LST_DISPO_EAU, LST_ASSAINISSEMENT, LST_CHAUFFE_EAU, LST_OUI_NON, LST_OUI_NON_INC

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_choices_logement(request):
    data = {
        'statut': [{'value': value, 'display': display} for value, display in LST_STATUT],
        'acces_final': [{'value': value, 'display': display} for value, display in LST_ACCES_FINAL],
        'propriete': [{'value': value, 'display': display} for value, display in LST_PROPRIETE],
        'type_logement': [{'value': value, 'display': display} for value, display in LST_TYPE_LOGEMENT],
        'multiusage': [{'value': value, 'display': display} for value, display in LST_MULTIUSAGE],
        'accueil_public': [{'value': value, 'display': display} for value, display in LST_ACCUEIL_PUBLIC],
        'activite_laitiere': [{'value': value, 'display': display} for value, display in LST_ACTIVITE_LAITIERE],
        'etat_batiment': [{'value': value, 'display': display} for value, display in LST_ETAT_BATIMENT],
        'mixite_possible': [{'value': value, 'display': display} for value, display in LST_OUI_NON_INC],
        'surface_logement': [{'value': value, 'display': display} for value, display in LST_SURFACE_LOGEMENT],
        'presence_douche': [{'value': value, 'display': display} for value, display in LST_OUI_NON_INC],
        'type_wc': [{'value': value, 'display': display} for value, display in LST_WC],
        'alim_elec': [{'value': value, 'display': display} for value, display in LST_ALIM_ELECTRIQUE],
        'alim_eau': [{'value': value, 'display': display} for value, display in LST_ALIM_EAU],
        'origine_eau': [{'value': value, 'display': display} for value, display in LST_ORIGINE_EAU],
        'qualite_eau': [{'value': value, 'display': display} for value, display in LST_QUALITE_EAU],
        'dispo_eau': [{'value': value, 'display': display} for value, display in LST_DISPO_EAU],
        'assainissement': [{'value': value, 'display': display} for value, display in LST_ASSAINISSEMENT],
        'chauffe_eau': [{'value': value, 'display': display} for value, display in LST_CHAUFFE_EAU],
        'chauffage': [{'value': value, 'display': display} for value, display in LST_OUI_NON],
        'stockage_indep': [{'value': value, 'display': display} for value, display in LST_OUI_NON],
        'qualite_eau': [{'value': value, 'display': display} for value, display in LST_QUALITE_EAU]
    }
    return Response(data)

# Droits utilisateurs / Permissions
class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Récupérer toutes les permissions de l'utilisateur
        user_permissions = user.get_all_permissions()
        
        # Récupérer les permissions détaillées
        all_permissions = Permission.objects.filter(codename__in=[
            perm.split('.')[1] for perm in user_permissions
        ]).select_related('content_type')
        
        # Grouper les permissions par modèle
        grouped_permissions = {}
        for perm in all_permissions:
            model = perm.content_type.model  # Le modèle auquel appartient la permission
            if model not in grouped_permissions:
                grouped_permissions[model] = []
            grouped_permissions[model].append(perm.codename)
        
        return Response({
            'username': user.username,
            'permissions_by_model': grouped_permissions,
        })


# Bloc administratif (orange)
class UnitePastoraleViewset(BaseModelViewSet):
    serializer_class = UnitePastoraleSerializer

    def get_queryset(self):
        queryset = UnitePastorale.objects.all().order_by('nom_up')
        
        nom_up_filter = self.request.GET.get('nom_up')
        if nom_up_filter is not None:
            queryset = queryset.filter(up_nom=nom_up_filter)
          
        return queryset

    # /unitePastorale/light/ → Serializer Light
    @action(detail=False, methods=['get'], url_path='light')
    def list_light(self, request):
        queryset = self.get_queryset()
        serializer = UnitePastoraleLSerializer(queryset, many=True)
        return Response(serializer.data)

   
class ProprietaireFoncierViewset(BaseModelViewSet):
    serializer_class = ProprietaireFoncierSerializer

    def get_queryset(self):
        queryset = ProprietaireFoncier.objects.all().order_by('id_proprietaire')
        return queryset
    
class EspeceViewset(BaseModelViewSet):
    serializer_class = EspeceSerializer

    def get_queryset(self):
        queryset = Espece.objects.all().order_by('id_espece')
        id_espece = self.request.GET.get('id_espece')
        if id_espece is not None:
            queryset = queryset.filter(id_espece=id_espece)

        return queryset
    def get_queryset(self):
        queryset = PlanDeSuivi.objects.all().select_related('type_suivi').select_related('unite_pastorale').order_by('id_plan_suivi')
        return queryset
    
    # @action(detail=False, methods=['get'])
    # def getNextId(self, request):
    #     # Récupérer le dernier ID dans la table et retourner le suivant
    #     last_plan = PlanDeSuivi.objects.order_by('id_plan_suivi').last()
    #     next_id = last_plan.id_plan_suivi + 1 if last_plan else 1
    #     return Response({'next_id': next_id})
    
    # def create(self, request, *args, **kwargs):
    #     logger.debug(f"Plan de suivi - Received data for creation: {request.data}")
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         logger.debug(f"Created instance: {serializer.data}")
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     logger.warning(f"Validation errors during creation: {serializer.errors}")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     logger.debug(f"Plan de suivi - Received data for update: {request.data}")
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         logger.debug(f"Updated instance: {serializer.data}")
    #         return Response(serializer.data)
    #     logger.warning(f"Validation errors during update: {serializer.errors}")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TypeDeMesureViewset(BaseModelViewSet):
    serializer_class = TypeDeMesureSerializer

    def get_queryset(self):
        queryset = TypeDeMesure.objects.all().order_by('id_type_mesure')
        return queryset
    
    # @action(detail=False, methods=['get'])
    # def getNextId(self, request):
    #     # Récupérer le dernier ID dans la table et retourner le suivant
    #     last_type = TypeDeMesure.objects.order_by('id_type_mesure').last()
    #     next_id = last_type.id_type_mesure + 1 if last_type else 1
    #     return Response({'next_id': next_id})
    
    # def create(self, request, *args, **kwargs):
    #     logger.debug(f"Type de mesure - Received data for creation: {request.data}")
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         logger.debug(f"Created instance: {serializer.data}")
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     logger.warning(f"Validation errors during creation: {serializer.errors}")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def update(self, request, *args, **kwargs):
    #     logger.debug(f"Type de mesure - Received data for update: {request.data}")
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         logger.debug(f"Updated instance: {serializer.data}")
    #         return Response(serializer.data)
    #     logger.warning(f"Validation errors during update: {serializer.errors}")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MesureDePlanViewset(BaseModelViewSet):
    serializer_class = MesureDePlanSerializer

    def get_queryset(self):
        queryset = MesureDePlan.objects.all().select_related('type_mesure').select_related('plan_suivi').order_by('id_mesure_plan')
        return queryset
    

# Bloc exploitation
class TypeConventionViewset(BaseModelViewSet):
    serializer_class = TypeConventionSerializer

    def get_queryset(self):
        queryset = TypeConvention.objects.all().order_by('id_type_convention')
        return queryset

class ConventionDExploitationViewset(BaseModelViewSet):
    serializer_class = ConventionDExploitationSerializer

    def get_queryset(self):
        queryset = ConventionDExploitation.objects.all().select_related('type_convention').order_by('id_convention')
        return queryset

class SituationDExploitationViewset(BaseModelViewSet):
    serializer_class = SituationDExploitationSerializer

    def get_queryset(self):
        queryset = SituationDExploitation.objects.all().order_by('id_situation')

        id_up_filter = self.request.GET.get('id_up')
        if id_up_filter is not None:
            queryset = queryset.filter(unite_pastorale_id=id_up_filter)
        return queryset
    @action(detail=True, methods=['post'], url_path='duplicate')
    def duplicate(self, request, pk=None):
        """
        Duplique une SituationDExploitation :
        - Met la situation d'origine en inactive et fixe sa date_fin à aujourd'hui
        - Crée une nouvelle situation copiée depuis l'origine, avec date_debut = aujourd'hui, date_fin = None et situation_active = True
        Retourne la nouvelle instance sérialisée.
        """
        from django.db import transaction
        from datetime import date

        try:
            orig = self.get_object()
        except Exception:
            return Response({'detail': 'Original situation not found.'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            # close original
            orig.date_fin = date.today()
            orig.situation_active = False
            orig.save()

            # compute next id
            last_situation = SituationDExploitation.objects.order_by('id_situation').last()
            next_id = last_situation.id_situation + 1 if last_situation else 1

            # duplicate fields (except PK and dates/active)
            new = SituationDExploitation()
            new.id_situation = next_id
            new.nom_situation = orig.nom_situation
            new.unite_pastorale = orig.unite_pastorale
            new.exploitant = orig.exploitant
            new.date_debut = date.today()
            new.date_fin = None
            new.situation_active = True
            new.save()

            # debug counts
            logger.debug(f"Orig related counts - exploitations={orig.exploitations.count()}, ruches={orig.ruches.count()}, gardes={orig.gardes_situation.count()}, elevers={getattr(orig, 'elevers').count() if hasattr(orig, 'elevers') else 'N/A'}")

            # Clone related objects: OUI exploitation des quartiers (Exploiter), PAS ruches (Ruche), PAS gardes_situation (GardeSituation), PAS eleveurs (Elever)
            # For each related object we create a copy linked to the new situation. For models that have date_debut/date_fin, set date_debut to today and date_fin to None.
            # Exploiter
            try:
                for ex in orig.exploitations.all():
                    last_ex = Exploiter.objects.order_by('id_exploiter').last()
                    next_ex_id = last_ex.id_exploiter + 1 if last_ex else 1
                    new_ex = Exploiter(
                        id_exploiter=next_ex_id,
                        quartier=ex.quartier,
                        situation_exploitation=new,
                        date_debut=date.today(),
                        date_fin=None,
                        commentaire=ex.commentaire,
                    )
                    new_ex.save()
            except Exception:
                # ignore if Exploiter model not present
                pass

            # Elever (livestock) - clone related Elever objects
            for el in orig.elevers.all():
                logger.debug(f"Cloning Elever id={getattr(el,'id_elever',None)} eleveur={getattr(el,'eleveur_id',None)}")
                last_el = Elever.objects.order_by('id_elever').last()
                next_el_id = last_el.id_elever + 1 if last_el else 1
                new_el = Elever(
                    id_elever=next_el_id,
                    situation_exploitation=new,
                    type_cheptel=el.type_cheptel,
                    eleveur=el.eleveur,
                    nombre_animaux=el.nombre_animaux,
                    pension=el.pension,
                    date_debut=date.today(),
                    date_fin=None,
                )
                new_el.save()

            # Ruche - clone beehives linked to the situation
            try:
                for ru in orig.ruches.all():
                    last_ru = Ruche.objects.order_by('id_ruche').last()
                    next_ru_id = last_ru.id_ruche + 1 if last_ru else 1
                    new_ru = Ruche(
                        id_ruche=next_ru_id,
                        description=ru.description,
                        geometry=ru.geometry,
                        situation_exploitation=new,
                    )
                    new_ru.save()
            except Exception:
                pass

            # GardeSituation - clone gardes linked to the situation
            try:
                for gr in orig.gardes_situation.all():
                    last_gr = GardeSituation.objects.order_by('id_garde_situation').last()
                    next_gr_id = last_gr.id_garde_situation + 1 if last_gr else 1
                    new_gr = GardeSituation(
                        id_garde_situation=next_gr_id,
                        date_debut=date.today(),
                        date_fin=None,
                        commentaire=gr.commentaire,
                        situation_exploitation=new,
                        berger=gr.berger,
                    )
                    new_gr.save()
            except Exception:
                pass

            serializer = self.get_serializer(new)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    


class Type_cheptelViewset(BaseModelViewSet):
    serializer_class = Type_cheptelSerializer

    def get_queryset(self):
        queryset = Type_cheptel.objects.all().order_by('id_type_cheptel')
        id_type_cheptel = self.request.GET.get('id_type_cheptel')
        if id_type_cheptel is not None:
            queryset = queryset.filter(id_type_cheptel=id_type_cheptel)

        return queryset
        queryset = TypeDExploitant.objects.all().order_by('id_type_exploitant')
        return queryset

class RaceViewset(BaseModelViewSet):
    serializer_class = RaceSerializer

    def get_queryset(self):
        queryset = Race.objects.all().order_by('id_race')
        id_race = self.request.GET.get('id_race')
        if id_race is not None:
            queryset = queryset.filter(id_race=id_race)

        return queryset

    def get_queryset(self):
        queryset = Ruche.objects.all().order_by('id_ruche')
        return queryset

class BergerViewset(BaseModelViewSet):
    serializer_class = BergerSerializer

    def get_queryset(self):
        queryset = Berger.objects.all().order_by('id_berger')
        return queryset

class GardeSituationViewset(BaseModelViewSet):
    serializer_class = GardeSituationSerializer

    def get_queryset(self):
        queryset = GardeSituation.objects.all().order_by('id_garde_situation')
        return queryset
 
class TypeCheptelViewset(BaseModelViewSet):
    serializer_class = TypeCheptelSerializer

    def get_queryset(self):
        queryset = TypeCheptel.objects.all().order_by('id_type_cheptel')
        return queryset

class EleverViewset(BaseModelViewSet):
    serializer_class = EleverSerializer

    def get_queryset(self):
        queryset = Elever.objects.all().select_related('eleveur').select_related('type_cheptel').order_by('id_elever')
        situation_id = self.request.GET.get('id_situation')
        if situation_id is not None:
            queryset = queryset.filter(situation_exploitation=situation_id)

        return queryset

# Evenements
class TypeEvenementViewset(BaseModelViewSet):
    serializer_class = TypeEvenementSerializer

    def get_queryset(self):
        queryset = TypeEvenement.objects.all().order_by('id_type_evenement')
        return queryset

class EvenementViewset(BaseModelViewSet):
    serializer_class = EvenementSerializer

    def get_queryset(self):
        queryset = Evenement.objects.all().order_by('id_evenement')
        return queryset
    
class LogementViewset(BaseModelViewSet):
    serializer_class = LogementSerializer

    def get_queryset(self):
        queryset = Logement.objects.all().order_by('id')

        logement_code = self.request.GET.get('logement_code')
        if logement_code is not None:
            queryset = queryset.filter(logement_code=logement_code)

        return queryset

class CommoditeViewset(BaseModelViewSet):
    serializer_class = CommoditeSerializer

    def get_queryset(self):
        queryset = Commodite.objects.all().order_by('id_commodite')

        return queryset
 
class LogementCommoditeViewset(BaseModelViewSet):
    serializer_class = LogementCommoditeSerializer

    def get_queryset(self):
        queryset = LogementCommodite.objects.all().order_by('id_logement_commodite')
        logement_id = self.request.GET.get('logementId')
        if logement_id is not None:
            queryset = queryset.filter(logement=logement_id)
        return queryset


class AbriDUrgenceCommoditeViewset(BaseModelViewSet):
    serializer_class = AbriDUrgenceCommoditeSerializer

    def get_queryset(self):
        queryset = AbriDUrgenceCommodite.objects.all().order_by('id_abri_urgence_commodite')
        abri_id = self.request.GET.get('abriId')
        if abri_id is not None:
            queryset =queryset.filter(abri_urgence=abri_id)
        return queryset



class TypeDeSuiviViewset(BaseModelViewSet):
    serializer_class = TypeDeSuiviSerializer

    def get_queryset(self):
        queryset = TypeDeSuivi.objects.all().order_by('id_type_suivi')
        return queryset
    
class TypeEquipementViewset(BaseModelViewSet):
    serializer_class = TypeEquipementSerializer
    
    def get_queryset(self):
        queryset = TypeEquipement.objects.all()
        return queryset

class EquipementAlpageViewset(BaseModelViewSet):
    serializer_class = EquipementAlpageSerializer

    def get_queryset(self):
        queryset = EquipementAlpage.objects.all().order_by('id_equipement_alpage')
        return queryset

class EquipementExploitantViewset(BaseModelViewSet):
    serializer_class = EquipementExploitantSerializer

    def get_queryset(self):
        queryset = EquipementExploitant.objects.all().order_by('id_equipement_exploitant')
        return queryset


###########
# Refactoring Elever et TypeCheptel pour les fusionner en Cheptel et Type_cheptel
# dlg le 10/2/26
class CheptelViewset(BaseModelViewSet):
    serializer_class = CheptelSerializer

    def get_queryset(self):
        queryset = Cheptel.objects.all().order_by('id_cheptel')
        id_cheptel = self.request.GET.get('id_cheptel')
        if id_cheptel is not None:
            queryset = queryset.filter(id_cheptel=id_cheptel)

        return queryset


class Type_cheptelViewset(BaseModelViewSet):
    serializer_class = Type_cheptelSerializer

    def get_queryset(self):
        queryset = Type_cheptel.objects.all().order_by('id_type_cheptel')
        return queryset


class Categorie_pensionViewset(BaseModelViewSet):
    serializer_class = Categorie_pensionSerializer

    def get_queryset(self):
        queryset = Categorie_pension.objects.all().order_by('id_categorie_pension')
        id_categorie_pension = self.request.GET.get('id_categorie_pension')
        if id_categorie_pension is not None:
            queryset = queryset.filter(id_categorie_pension=id_categorie_pension)

        return queryset


class EspeceViewset(BaseModelViewSet):
    serializer_class = EspeceSerializer

    def get_queryset(self):
        queryset = Espece.objects.all().order_by('id_espece')
        return queryset


class RaceViewset(BaseModelViewSet):
    serializer_class = RaceSerializer

    def get_queryset(self):
        queryset = Race.objects.all().order_by('id_race')
        return queryset


class Categorie_animauxViewset(BaseModelViewSet):
    serializer_class = Categorie_animauxSerializer

    def get_queryset(self):
        queryset = Categorie_animaux.objects.all().order_by('id_categorie_animaux')
        return queryset
    
# Refactoring Elever et TypeCheptel pour les fusionner en Cheptel et Type_cheptel
# dlg le 10/2/26
###########

# Restored historical viewsets (from removed_viewsets_review.py)
class UPProprietaireViewset(BaseModelViewSet):
    serializer_class = UPProprietaireSerializer

    def get_queryset(self):
        queryset = UPProprietaire.objects.all().order_by('id_up_proprietaire')
        return queryset

class QuartierPastoViewset(BaseModelViewSet):
    serializer_class = QuartierPastoSerializer

    def get_queryset(self):
        queryset = QuartierPasto.objects.all().order_by('unite_pastorale', 'code_quartier')

        up_id = self.request.GET.get('up_id')
        if up_id is not None:
            queryset = queryset.filter(unite_pastorale=up_id)

        return queryset

class PlanDeSuiviViewset(BaseModelViewSet):
    serializer_class = PlanDeSuiviSerializer

    def get_queryset(self):
        queryset = PlanDeSuivi.objects.all().select_related('type_suivi').select_related('unite_pastorale').order_by('id_plan_suivi')
        return queryset

class ExploiterViewset(BaseModelViewSet):
    serializer_class = ExploiterSerializer

    def get_queryset(self):
        queryset = Exploiter.objects.all().order_by('id_exploiter')
        return queryset

class EleveurViewset(BaseModelViewSet):
    serializer_class = EleveurSerializer

    def get_queryset(self):
        queryset = Eleveur.objects.all().order_by('nom_eleveur')
        return queryset

    @action(detail=False, methods=['get'], url_path='by-exploitant/(?P<expl_id>[^/.]+)')
    def by_exploitant(self, request, expl_id=None):
        # Récupérer tous les EtreCompose pour l'exploitant
        compositions = EtreCompose.objects.filter(exploitant_id=expl_id).select_related('eleveur')
        eleveurs = [c.eleveur for c in compositions if c.eleveur is not None]

        # Sérialiser manuellement
        data = [
            {
                "id_eleveur": e.id_eleveur,
                "nom_eleveur": e.nom_eleveur,
                "prenom_eleveur": e.prenom_eleveur,
            }
            for e in eleveurs
        ]
        return Response(data)

class TypeDExploitantViewset(BaseModelViewSet):
    serializer_class = TypeDExploitantSerializer

    def get_queryset(self):
        queryset = TypeDExploitant.objects.all().order_by('id_type_exploitant')
        return queryset

class ExploitantViewset(BaseModelViewSet):
    serializer_class = ExploitantSerializer

    def get_queryset(self):
        queryset = Exploitant.objects.all().select_related('type_exploitant').order_by('id_exploitant')
        return queryset

class EtreComposeViewset(BaseModelViewSet):
    serializer_class = EtreComposeSerializer

    def get_queryset(self):
        queryset = EtreCompose.objects.all().order_by('id')
        return queryset

class SubventionPNVViewset(BaseModelViewSet):
    serializer_class = SubventionPNVSerializer

    def get_queryset(self):
        queryset = SubventionPNV.objects.all().select_related('exploitant').order_by('id_subvention')
        return queryset

class AbriDUrgenceViewset(BaseModelViewSet):
    serializer_class = AbriDUrgenceSerializer

    def get_queryset(self):
        queryset = AbriDUrgence.objects.all().order_by('id_abri_urgence')
        return queryset

class BeneficierDeViewset(BaseModelViewSet):
    serializer_class = BeneficierDeSerializer

    def get_queryset(self):
        queryset = BeneficierDe.objects.all().order_by('id_beneficier_de')
        return queryset

class RucheViewset(BaseModelViewSet):
    serializer_class = RucheSerializer

    def get_queryset(self):
        queryset = Ruche.objects.all().order_by('id_ruche')
        return queryset

class ProductionViewset(BaseModelViewSet):
    serializer_class = ProductionSerializer

    def get_queryset(self):
        queryset = Production.objects.all().order_by('id_production')
        return queryset

