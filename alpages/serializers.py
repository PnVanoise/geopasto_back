from django.db import transaction

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from django.contrib.gis.geos import Polygon

from alpages.models import Logement, QuartierUP, Quartieralpage, Commodite, LogementCommodite
from alpages.models import UnitePastorale, ProprietaireFoncier, QuartierPasto, UPProprietaire
from alpages.models import TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan
from alpages.models import TypeConvention, ConventionDExploitation, Eleveur, Exploitant, EtreCompose, SubventionPNV, AbriDUrgence, BeneficierDe
from alpages.models import SituationDExploitation, Exploiter
from alpages.models import Ruche, Berger, TypeCheptel, GardeSituation, Elever
from alpages.models import TypeEvenement, Evenement

from alpages.models import LogementTest


# Bloc administratif (orange)
class UnitePastoraleSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = UnitePastorale
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)

class ProprietaireFoncierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProprietaireFoncier
        fields = [ 'id_proprietaire', 'nom_propr', 'prenom_propr',
                  'tel_propr', 'mail_propr', 'adresse_propr', 'commentaire', 'unites_pastorales' ]

class UPProprietaireSerializer(serializers.ModelSerializer):
    up_nom = serializers.CharField(source='unite_pastorale.nom_up', read_only=True)
    proprietaire_nom = serializers.CharField(source='proprietaire.nom_propr', read_only=True)
    
    class Meta:
        model = UPProprietaire
        fields = [ 'id_up_proprietaire', 'unite_pastorale', 'proprietaire', 'up_nom', 'proprietaire_nom' ]
    
class QuartierPastoSerializer(GeoFeatureModelSerializer):
    unitepastorale_nom = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = QuartierPasto
        geo_field = 'geometry'
        auto_bbox = True
        fields = ['id_quartier', 'code_quartier', 'nom_quartier', 'geometry', 'unite_pastorale', 'unitepastorale_nom']
        
    def get_unitepastorale_nom(self, obj):
        return obj.unite_pastorale.nom_up if obj.unite_pastorale else None

    def to_internal_value(self, data):
        # Intercepter les données de géométrie avant la validation
        geometry = data.get('geometry', None)

        # Vérifier si les coordonnées sont vides et définir geometry sur None si c'est le cas
        if geometry and geometry.get('type') == 'Polygon' and not geometry.get('coordinates'):
            data['geometry'] = None

        return super().to_internal_value(data)

    def to_representation(self, instance):
        if instance.geometry is not None:
            instance.geometry.transform(4326)

        data = super().to_representation(instance)

        # Vérifiez si la géométrie est None et renvoyez un objet géométrique par défaut
        if instance.geometry is None:
            data['geometry'] = {
                "type": "Polygon",
                "coordinates": [[]]  # Un polygone vide
            }
        
        if instance.unite_pastorale is None:
            data['unitepastorale_nom'] = None

        return data

# Bloc plans de suivi (bleu)
class TypeDeSuiviSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeDeSuivi
        fields = [ 'id_type_suivi', 'description' ]
    
class PlanDeSuiviSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlanDeSuivi
        fields = [ 'id_plan_suivi', 'description', 'date_debut', 'date_fin', 'type_suivi', 'unite_pastorale' ]

class TypeDeMesureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeDeMesure
        fields = [ 'id_type_mesure', 'description' ]

class MesureDePlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MesureDePlan
        fields = [ 'id_mesure_plan', 'description', 'commentaire', 'debut_periode', 'fin_periode', 'type_mesure', 'plan_suivi' ]

# Bloc expoitation
class TypeConventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeConvention
        fields = [ 'id_type_convention', 'description' ]

class ConventionDExploitationSerializer(GeoFeatureModelSerializer):
    exploitant_nom = serializers.CharField(source='exploitant.nom_exploitant', read_only=True)
    up_nom = serializers.CharField(source='unite_pastorale.nom_up', read_only=True)
    
    class Meta:
        model = ConventionDExploitation
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)

class SituationDExploitationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SituationDExploitation
        fields = [ 'id_situation', 'nom_situation', 'situation_active', 'date_debut', 'date_fin', 'exploitant', 'unite_pastorale' ]
    
class ExploiterSerializer(serializers.ModelSerializer):
    
    situation_nom = serializers.CharField(source='situation_exploitation.nom_situation', read_only=True)
    quartier_nom = serializers.CharField(source='quartier.nom_quartier', read_only=True)
    
    
    class Meta:
        model = Exploiter
        fields = [ 'id_exploiter', 'date_debut', 'date_fin', 'quartier', 'situation_exploitation', 'commentaire',
                  'situation_nom', 'quartier_nom' ]
            

class EleveurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Eleveur
        fields = [ 'id_eleveur', 'nom_eleveur', 'prenom_eleveur', 'adresse_eleveur', 'tel_eleveur', 'mail_eleveur', 'commentaire' ]
        
class ExploitantSerializer(serializers.ModelSerializer):
    membres = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    membres_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Exploitant
        fields = ['id_exploitant', 'nom_exploitant', 'type', 'president', 'membres', 'membres_ids']

    def get_membres_ids(self, obj):
        # Récupérer uniquement les IDs des éleveurs associés via la table `EtreCompose`
        membres = EtreCompose.objects.filter(exploitant=obj).values_list('eleveur_id', flat=True)
        return list(membres)

    def create(self, validated_data):
        membres_data = validated_data.pop('membres', [])
        exploitant = Exploitant.objects.create(**validated_data)
        
        # Ajout des membres dans la table EtreCompose
        for eleveur_id in membres_data:
            eleveur = Eleveur.objects.get(id_eleveur=eleveur_id)
            EtreCompose.objects.create(exploitant=exploitant, eleveur=eleveur)

        return exploitant

    def update(self, instance, validated_data):
        membres_data = validated_data.pop('membres', [])
        instance.nom_exploitant = validated_data.get('nom_exploitant', instance.nom_exploitant)
        instance.type = validated_data.get('type', instance.type)
        instance.president = validated_data.get('president', instance.president)
        
        with transaction.atomic():
            instance.save()

            # Récupérer les IDs actuels des membres de l'exploitant
            membres_actuels = set(EtreCompose.objects.filter(exploitant=instance).values_list('eleveur_id', flat=True))
            nouveaux_membres = set(membres_data)

            # Supprimer les membres qui ne sont plus associés
            membres_a_supprimer = membres_actuels - nouveaux_membres
            if membres_a_supprimer:
                EtreCompose.objects.filter(exploitant=instance, eleveur_id__in=membres_a_supprimer).delete()

            # Ajouter les nouveaux membres
            membres_a_ajouter = nouveaux_membres - membres_actuels
            for eleveur_id in membres_a_ajouter:
                eleveur = Eleveur.objects.get(id_eleveur=eleveur_id)
                EtreCompose.objects.create(exploitant=instance, eleveur=eleveur)

        return instance

       
class EtreComposeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EtreCompose
        fields = [ 'exploitant', 'eleveur' ]

class SubventionPNVSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubventionPNV
        fields = [ 'id_subvention', 'description', 'montant', 'engage', 'paye', 'exploitant' ]

class LogementSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Logement
        geo_field = 'geom'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geom != None):
            instance.geom.transform(4326)
        
        return super().to_representation(instance)

class CommoditeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Commodite
        fields = [ 'id_commodite', 'description']

class LogementCommoditeSerializer(serializers.ModelSerializer):
    logement_code = serializers.CharField(source='logement.logement_code', read_only=True)
    commodite_desc = serializers.CharField(source='commodite.description', read_only=True)
    
    class Meta:
        model = LogementCommodite
        fields = [ 'id_logement_commodite', 'logement', 'commodite', 'etat', 'commentaire', 'quantite', 'logement_code', 'commodite_desc' ]
        

class AbriDUrgenceSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = AbriDUrgence
            fields = [ 'id_abri_urgence', 'description', 'etat', 'created_by', 'created_on', 'modified_by', 'modified_on' ]        
            
class BeneficierDeSerializer(GeoFeatureModelSerializer):
    
    exploitant_nom = serializers.CharField(source='exploitant.nom_exploitant', read_only=True)
    abri_description = serializers.CharField(source='abri_urgence.description', read_only=True)
    
    class Meta:
        model = BeneficierDe
        geo_field = 'geometry'
        auto_bbox = True
        fields = [
            'id_beneficier_de', 'exploitant', 'abri_urgence', 'date_debut', 'date_fin', 'geometry',
            'exploitant_nom', 'abri_description'
        ]
    
    def to_internal_value(self, data):
        # Intercepter les données de géométrie avant la validation
        geometry = data.get('geometry', None)

        # Vérifier si les coordonnées sont vides et définir geometry sur None si c'est le cas
        if geometry and geometry.get('type') == 'Point' and not geometry.get('coordinates'):
            data['geometry'] = None

        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)

# Ruche / Berger / type_cheptel
class RucheSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Ruche
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)

class BergerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Berger
        fields = [ 'id_berger', 'nom_berger', 'prenom_berger', 'adresse_berger', 'tel_berger', 'commentaire' ]

class GardeSituationSerializer(serializers.ModelSerializer):
    
    berger_nom = serializers.CharField(source='berger.nom_berger', read_only=True)
    berger_prenom = serializers.CharField(source='berger.prenom_berger', read_only=True)
    situation_nom = serializers.CharField(source='situation_exploitation.nom_situation', read_only=True)
    
    class Meta:
        model = GardeSituation
        fields = [ 'id_garde_situation', 'date_debut', 'date_fin', 'commentaire', 'situation_exploitation', 'berger',
                  'situation_nom', 'berger_nom', 'berger_prenom' ]


class TypeCheptelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeCheptel
        fields = [ 'id_type_cheptel', 'description', 'espece', 'race', 'production', 'stade_maturite', 'pension' ]

class EleverSerializer(serializers.ModelSerializer):
    
    type_cheptel_description = serializers.CharField(source='type_cheptel.description', read_only=True)
    eleveur_nom = serializers.CharField(source='eleveur.nom_eleveur', read_only=True)
    eleveur_prenom = serializers.CharField(source='eleveur.prenom_eleveur', read_only=True)
    situation_nom = serializers.CharField(source='situation_exploitation.nom_situation', read_only=True)
    
    class Meta:
        model = Elever
        fields = [ 'id_elever', 'date_debut', 'date_fin', 'nombre_animaux', 'type_cheptel', 'eleveur', 'situation_exploitation',
                  'type_cheptel_description', 'eleveur_nom', 'eleveur_prenom', 'situation_nom' ]
    
# Evenements
class TypeEvenementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeEvenement
        fields = [ 'id_type_evenement', 'description' ]


class EvenementSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Evenement
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)

# TEMPORAIRE DLG
class QuartieralpageSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Quartieralpage
        geo_field = 'geom'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geom != None):
            instance.geom.transform(4326)
        
        return super().to_representation(instance)
            
class QuartierUPSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = QuartierUP
        geo_field = 'geom'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geom != None):
            instance.geom.transform(4326)
            return super().to_representation(instance)
        else:
            return ""


# TEST CC
#IMPORTER classe du model
class LogementTestSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = LogementTest
        geo_field = 'geometry'
        fields = '__all__'
    
    # Transformation du 2154 vers 4326
    def to_representation(self, instance):
        if instance.geometry:
            instance.geometry.transform(4326)
        return super().to_representation(instance)