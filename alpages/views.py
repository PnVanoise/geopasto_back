# from rest_framework.views import APIView
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import api_view, action

from alpages.models import Logement, QuartierUP, Quartieralpage, Commodite, LogementCommodite
from alpages.models import UnitePastorale, ProprietaireFoncier, QuartierPasto, UPProprietaire
from alpages.models import TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan
from alpages.models import TypeConvention, ConventionDExploitation, Eleveur, Exploitant, EtreCompose, SubventionPNV, AbriDUrgence, BeneficierDe
from alpages.models import SituationDExploitation, Exploiter

from alpages.models import Ruche, Berger, TypeCheptel, GardeSituation, Elever
from alpages.serializers import RucheSerializer, BergerSerializer, TypeCheptelSerializer, GardeSituationSerializer, EleverSerializer

from alpages.models import TypeEvenement, Evenement
from alpages.serializers import TypeEvenementSerializer, EvenementSerializer

from alpages.serializers import LogementSerializer, QuartierUPSerializer, QuartieralpageSerializer, CommoditeSerializer, LogementCommoditeSerializer
from alpages.serializers import UnitePastoraleSerializer, ProprietaireFoncierSerializer, QuartierPastoSerializer, UPProprietaireSerializer
from alpages.serializers import TypeDeSuiviSerializer, PlanDeSuiviSerializer, TypeDeMesureSerializer, MesureDePlanSerializer
from alpages.serializers import TypeConventionSerializer, ConventionDExploitationSerializer, EleveurSerializer, ExploitantSerializer, EtreComposeSerializer, SubventionPNVSerializer, AbriDUrgenceSerializer, BeneficierDeSerializer
from alpages.serializers import SituationDExploitationSerializer, ExploiterSerializer

from alpages.models import LogementTest
from alpages.serializers import LogementTestSerializer


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

# Bloc administratif (orange)
class UnitePastoraleViewset(ModelViewSet):
    serializer_class = UnitePastoraleSerializer

    def get_queryset(self):
        queryset = UnitePastorale.objects.all().order_by('nom_up')
        
        nom_up_filter = self.request.GET.get('nom_up')
        if nom_up_filter is not None:
            queryset = queryset.filter(up_nom=nom_up_filter)
          
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_UP = UnitePastorale.objects.order_by('id_unite_pastorale').last()
        next_id = last_UP.id_unite_pastorale + 1 if last_UP else 1
        return Response({'next_id': next_id})
     
    def create(self, request, *args, **kwargs):
        logger.debug(f"Unite Pastorale - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Unite Pastorale - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class ProprietaireFoncierViewset(ModelViewSet):
    serializer_class = ProprietaireFoncierSerializer

    def get_queryset(self):
        queryset = ProprietaireFoncier.objects.all().order_by('id_proprietaire')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_propr = ProprietaireFoncier.objects.order_by('id_proprietaire').last()
        next_id = last_propr.id_proprietaire + 1 if last_propr else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Proprietaire Foncier - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Proprietaire Foncier - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UPProprietaireViewset(ModelViewSet):
    serializer_class = UPProprietaireSerializer

    def get_queryset(self):
        queryset = UPProprietaire.objects.all().order_by('id_up_proprietaire')
        return queryset
        
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_up_propr = UPProprietaire.objects.order_by('id_up_proprietaire').last()
        next_id = last_up_propr.id_up_proprietaire + 1 if last_up_propr else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"UP Proprietaire - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"UP Proprietaire - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class QuartierPastoViewset(ModelViewSet):
    serializer_class = QuartierPastoSerializer
    
    def get_queryset(self):
        queryset = QuartierPasto.objects.all().order_by('unite_pastorale', 'code_quartier')
        
        up_id = self.request.GET.get('up_id')
        if up_id is not None:
            queryset = queryset.filter(unite_pastorale=up_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_quartier = QuartierPasto.objects.order_by('id_quartier').last()
        next_id = last_quartier.id_quartier + 1 if last_quartier else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Quartier Pastoral - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Quartier Pastoral - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bloc plans de suivi (bleu)
class TypeDeSuiviViewset(ModelViewSet):
    serializer_class = TypeDeSuiviSerializer

    def get_queryset(self):
        queryset = TypeDeSuivi.objects.all().order_by('id_type_suivi')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_type = TypeDeSuivi.objects.order_by('id_type_suivi').last()
        next_id = last_type.id_type_suivi + 1 if last_type else 1
        return Response({'next_id': next_id})

class PlanDeSuiviViewset(ModelViewSet):
    serializer_class = PlanDeSuiviSerializer

    def get_queryset(self):
        queryset = PlanDeSuivi.objects.all().order_by('id_plan_suivi')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_plan = PlanDeSuivi.objects.order_by('id_plan_suivi').last()
        next_id = last_plan.id_plan_suivi + 1 if last_plan else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Plan de suivi - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Plan de suivi - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TypeDeMesureViewset(ModelViewSet):
    serializer_class = TypeDeMesureSerializer

    def get_queryset(self):
        queryset = TypeDeMesure.objects.all().order_by('id_type_mesure')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_type = TypeDeMesure.objects.order_by('id_type_mesure').last()
        next_id = last_type.id_type_mesure + 1 if last_type else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Type de mesure - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Type de mesure - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MesureDePlanViewset(ModelViewSet):
    serializer_class = MesureDePlanSerializer

    def get_queryset(self):
        queryset = MesureDePlan.objects.all().order_by('id_mesure_plan')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_mesure = MesureDePlan.objects.order_by('id_mesure_plan').last()
        next_id = last_mesure.id_mesure_plan + 1 if last_mesure else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Mesure de plan - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Mesure de plan - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bloc exploitation
class TypeConventionViewset(ModelViewSet):
    serializer_class = TypeConventionSerializer

    def get_queryset(self):
        queryset = TypeConvention.objects.all().order_by('id_type_convention')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_type = TypeConvention.objects.order_by('id_type_convention').last()
        next_id = last_type.id_type_convention + 1 if last_type else 1
        return Response({'next_id': next_id})

class ConventionDExploitationViewset(ModelViewSet):
    serializer_class = ConventionDExploitationSerializer

    def get_queryset(self):
        queryset = ConventionDExploitation.objects.all().order_by('id_convention')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_convention = ConventionDExploitation.objects.order_by('id_convention').last()
        next_id = last_convention.id_convention + 1 if last_convention else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Convention d'exploitation - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Convention d'exploitation - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SituationDExploitationViewset(ModelViewSet):
    serializer_class = SituationDExploitationSerializer

    # def get_queryset(self):
    #     queryset = UnitePastorale.objects.all().order_by('nom_up')
        
    #     nom_up_filter = self.request.GET.get('nom_up')
    #     if nom_up_filter is not None:
    #         queryset = queryset.filter(up_nom=nom_up_filter)
          
    #     return queryset
    
    
    def get_queryset(self):
        queryset = SituationDExploitation.objects.all().order_by('id_situation')
        
        id_up_filter = self.request.GET.get('id_up')
        if id_up_filter is not None:
            queryset = queryset.filter(unite_pastorale_id=id_up_filter)
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_situation = SituationDExploitation.objects.order_by('id_situation').last()
        next_id = last_situation.id_situation + 1 if last_situation else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Situation d'exploitation - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Situation d'exploitation - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExploiterViewset(ModelViewSet):
    serializer_class = ExploiterSerializer

    def get_queryset(self):
        queryset = Exploiter.objects.all().order_by('id_exploiter')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_exploiter = Exploiter.objects.order_by('id_exploiter').last()
        next_id = last_exploiter.id_exploiter + 1 if last_exploiter else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Exploiter - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Exploiter - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EleveurViewset(ModelViewSet):
    serializer_class = EleveurSerializer

    def get_queryset(self):
        queryset = Eleveur.objects.all().order_by('nom_eleveur')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_eleveur = Eleveur.objects.order_by('id_eleveur').last()
        next_id = last_eleveur.id_eleveur + 1 if last_eleveur else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Eleveur - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Eleveur - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExploitantViewset(ModelViewSet):
    serializer_class = ExploitantSerializer

    def get_queryset(self):
        queryset = Exploitant.objects.all().order_by('id_exploitant')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_exploitant = Exploitant.objects.order_by('id_exploitant').last()
        next_id = last_exploitant.id_exploitant + 1 if last_exploitant else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Exploitant - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Exploitant - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EtreComposeViewset(ModelViewSet):
    serializer_class = EtreComposeSerializer

    def get_queryset(self):
        queryset = EtreCompose.objects.all().order_by('id')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_ec = EtreCompose.objects.order_by('id').last()
        next_id = last_ec.id + 1 if last_ec else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"EtreCompose - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"EtreCompose - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubventionPNVViewset(ModelViewSet):
    serializer_class = SubventionPNVSerializer

    def get_queryset(self):
        queryset = SubventionPNV.objects.all().order_by('id_subvention')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_subvention = SubventionPNV.objects.order_by('id_subvention').last()
        next_id = last_subvention.id_subvention + 1 if last_subvention else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Subvention PNV - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Subvention PNV - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AbriDUrgenceViewset(ModelViewSet):
    serializer_class = AbriDUrgenceSerializer

    def get_queryset(self):
        queryset = AbriDUrgence.objects.all().order_by('id_abri_urgence')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_abri = AbriDUrgence.objects.order_by('id_abri_urgence').last()
        next_id = last_abri.id_abri_urgence + 1 if last_abri else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Abri d'urgence - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Abri d'urgence - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class BeneficierDeViewset(ModelViewSet):
    serializer_class = BeneficierDeSerializer

    def get_queryset(self):
        queryset = BeneficierDe.objects.all().order_by('id_beneficier_de')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_benef = BeneficierDe.objects.order_by('id_beneficier_de').last()
        next_id = last_benef.id_beneficier_de + 1 if last_benef else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Beneficier de - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Beneficier de - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Ruche / Berger / type_cheptel
class RucheViewset(ModelViewSet):
    serializer_class = RucheSerializer

    def get_queryset(self):
        queryset = Ruche.objects.all().order_by('id_ruche')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_ruche = Ruche.objects.order_by('id_ruche').last()
        next_id = last_ruche.id_ruche + 1 if last_ruche else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Ruche - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Ruche - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BergerViewset(ModelViewSet):
    serializer_class = BergerSerializer

    def get_queryset(self):
        queryset = Berger.objects.all().order_by('id_berger')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_berger = Berger.objects.order_by('id_berger').last()
        next_id = last_berger.id_berger + 1 if last_berger else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Berger - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Berger - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GardeSituationViewset(ModelViewSet):
    serializer_class = GardeSituationSerializer

    def get_queryset(self):
        queryset = GardeSituation.objects.all().order_by('id_garde_situation')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_garde = GardeSituation.objects.order_by('id_garde_situation').last()
        next_id = last_garde.id_garde_situation + 1 if last_garde else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Garde situation - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Garde situation - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class TypeCheptelViewset(ModelViewSet):
    serializer_class = TypeCheptelSerializer

    def get_queryset(self):
        queryset = TypeCheptel.objects.all().order_by('id_type_cheptel')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_type = TypeCheptel.objects.order_by('id_type_cheptel').last()
        next_id = last_type.id_type_cheptel + 1 if last_type else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Type de cheptel - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Type de cheptel - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EleverViewset(ModelViewSet):
    serializer_class = EleverSerializer

    def get_queryset(self):
        queryset = Elever.objects.all().order_by('id_elever')
        situation_id = self.request.GET.get('id_situation')
        if situation_id is not None:
            queryset = queryset.filter(situation_exploitation=situation_id)
        
        return queryset
    
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_elever = Elever.objects.order_by('id_elever').last()
        next_id = last_elever.id_elever + 1 if last_elever else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Elever - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Elever - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Evenements
class TypeEvenementViewset(ModelViewSet):
    serializer_class = TypeEvenementSerializer

    def get_queryset(self):
        queryset = TypeEvenement.objects.all().order_by('id_type_evenement')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_type = TypeEvenement.objects.order_by('id_type_evenement').last()
        next_id = last_type.id_type_evenement + 1 if last_type else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Type d'événement - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Type d'événement - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvenementViewset(ModelViewSet):
    serializer_class = EvenementSerializer

    def get_queryset(self):
        queryset = Evenement.objects.all().order_by('id_evenement')
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_evenement = Evenement.objects.order_by('id_evenement').last()
        next_id = last_evenement.id_evenement + 1 if last_evenement else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Evenement - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Evenement - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogementViewset(ModelViewSet):
    serializer_class = LogementSerializer

    def get_queryset(self):
        queryset = Logement.objects.all().order_by('id')
        
        logement_code = self.request.GET.get('logement_code')
        if logement_code is not None:
            queryset = queryset.filter(logement_code=logement_code)
          
        return queryset
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Logement - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Logement - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommoditeViewset(ModelViewSet):
    serializer_class = CommoditeSerializer

    def get_queryset(self):
        queryset = Commodite.objects.all().order_by('id_commodite')
        
        return queryset

    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_commodite = Commodite.objects.order_by('id_commodite').last()
        next_id = last_commodite.id_commodite + 1 if last_commodite else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"Commodite - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Commodite - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class LogementCommoditeViewset(ModelViewSet):
    serializer_class = LogementCommoditeSerializer

    def get_queryset(self):
        queryset = LogementCommodite.objects.all().order_by('id_logement_commodite')
        logement_id = self.request.GET.get('logementId')
        if logement_id is not None:
            queryset = queryset.filter(logement=logement_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def getNextId(self, request):
        # Récupérer le dernier ID dans la table et retourner le suivant
        last_logement_commodite = LogementCommodite.objects.order_by('id_logement_commodite').last()
        next_id = last_logement_commodite.id_logement_commodite + 1 if last_logement_commodite else 1
        return Response({'next_id': next_id})
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"LogementCommodite - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"LogementCommodite - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuartierUPViewset(ModelViewSet):
    serializer_class = QuartierUPSerializer

    def get_queryset(self):
        queryset = QuartierUP.objects.all().order_by('id')
        
        nom_up = self.request.GET.get('nom_up')
        if nom_up is not None:
            queryset = queryset.filter(up_nom_1=nom_up)
          
        return queryset
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"QuartierUP - Received data for creation: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.debug(f"Created instance: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.warning(f"Validation errors during creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.debug(f"QuartierUP - Received data for update: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Updated instance: {serializer.data}")
            return Response(serializer.data)
        logger.warning(f"Validation errors during update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuartieralpageViewset(ModelViewSet):
    serializer_class = QuartieralpageSerializer

    def get_queryset(self):
        queryset = Quartieralpage.objects.all()
        return queryset

# TEST CC
# IMPORTER classe du model et du serializer
class LogementTestViewset(ModelViewSet):
    serializer_class = LogementTestSerializer

    # Personnalisation de la requete executée
    def get_queryset(self):
        queryset = LogementTest.objects.all()
        return queryset