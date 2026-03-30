from django.db import transaction

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.functions import Distance

from alpages.models import Logement, QuartierUP, Quartieralpage, Commodite, LogementCommodite
from alpages.models import UnitePastorale, ProprietaireFoncier, QuartierPasto, UPProprietaire
from alpages.models import TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan
from alpages.models import TypeConvention, ConventionDExploitation, Eleveur, TypeDExploitant, Exploitant, EtreCompose, SubventionPNV, AbriDUrgence, AbriDUrgenceCommodite, BeneficierDe
from alpages.models import SituationDExploitation, Exploiter
from alpages.models import Ruche, Berger, TypeCheptel, GardeSituation, Elever
from alpages.models import TypeEvenement, Evenement
from alpages.models import TypeEquipement, EquipementAlpage, EquipementExploitant
from alpages.models import Production, Categorie_pension, Race, Categorie_animaux, Espece, Cheptel, Type_cheptel

from alpages.models import LogementTest


# Bloc administratif (orange)
class UnitePastoraleSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = UnitePastorale
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        geom = getattr(instance, 'geometry', None)
        if geom is not None:
            try:
                geom.transform(4326)
            except Exception:
                # protect against invalid/None geometries that may raise during transform
                pass

        return super().to_representation(instance)

# light serializer, pour les listes
class UnitePastoraleLSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UnitePastorale
        fields = [ 'id_unite_pastorale', 'nom_up', 'secteur' ]


class ProprietaireFoncierSerializer(serializers.ModelSerializer):
    unites_pastorales = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
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
    unite_pastorale = serializers.PrimaryKeyRelatedField(
        queryset = UnitePastorale.objects.all(),
        allow_null = True
    )
    unite_pastorale_detail = UnitePastoraleLSerializer(
        source='unite_pastorale',
        read_only=True
    )
    type_suivi = serializers.PrimaryKeyRelatedField(
        queryset = TypeDeSuivi.objects.all(),
        allow_null=True
    )
    type_suivi_detail = TypeDeSuiviSerializer(
        source = 'type_suivi',
        read_only = True
    )
    class Meta:
        model = PlanDeSuivi
        fields = [ 'id_plan_suivi', 'description', 'date_debut', 'date_fin', 'type_suivi', 'type_suivi_detail', 'unite_pastorale', 'unite_pastorale_detail' ]

class TypeDeMesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDeMesure
        fields = [ 'id_type_mesure', 'description' ]

class MesureDePlanSerializer(serializers.ModelSerializer):
    plan_suivi = serializers.PrimaryKeyRelatedField(
        queryset = PlanDeSuivi.objects.all(),
        allow_null = True
    )
    plan_suivi_detail = PlanDeSuiviSerializer(
        source = 'plan_suivi',
        read_only = True
    )
    type_mesure = serializers.PrimaryKeyRelatedField(
        queryset = TypeDeMesure.objects.all(),
        allow_null = True,
    )
    type_mesure_detail = TypeDeMesureSerializer(
        source = 'type_mesure',
        read_only = True
    )
    class Meta:
        model = MesureDePlan
        fields = [ 'id_mesure_plan', 'description', 'commentaire', 'debut_periode', 'fin_periode', 'type_mesure', 'type_mesure_detail', 'plan_suivi', 'plan_suivi_detail' ]

# Bloc expoitation
class TypeConventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeConvention
        fields = [ 'id_type_convention', 'description' ]

class ConventionDExploitationSerializer(GeoFeatureModelSerializer):
    type_convention = serializers.PrimaryKeyRelatedField(
        queryset = TypeConvention.objects.all(), allow_null = True
    )
    type_convention_detail = TypeConventionSerializer(source='type_convention', read_only=True)
    
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

    unite_pastorale = serializers.PrimaryKeyRelatedField(
        queryset = UnitePastorale.objects.all(),
        allow_null = True,
    )
    unite_pastorale_detail = UnitePastoraleLSerializer(
        source='unite_pastorale',
        read_only=True,
    )

    exploitant_nom = serializers.SerializerMethodField()

    def get_exploitant_nom(self, obj):
        return obj.exploitant.nom_exploitant if obj.exploitant else None
    
    class Meta:
        model = SituationDExploitation
        fields = [ 'id_situation', 'nom_situation', 'situation_active', 'date_debut', 'date_fin',
                  'exploitant', 'exploitant_nom', 'unite_pastorale', 'unite_pastorale_detail' ]
    

class ExploiterSerializer(serializers.ModelSerializer):
    
    situation_nom = serializers.CharField(source='situation_exploitation.nom_situation', read_only=True)
    quartier_nom = serializers.CharField(source='quartier.nom_quartier', read_only=True)
       
    class Meta:
        model = Exploiter
        fields = [ 'id_exploiter', 'date_debut', 'date_fin', 'quartier', 'situation_exploitation', 'commentaire',
                  'situation_nom', 'quartier_nom' ]
            

class EleveurSerializer(serializers.ModelSerializer):

    nom_complet = serializers.SerializerMethodField()
    
    class Meta:
        model = Eleveur
        read_only_fields = ['id_eleveur']
        fields = [ 'id_eleveur', 'nom_eleveur', 'prenom_eleveur', 'adresse_eleveur', 'tel_eleveur', 'mail_eleveur', 'commentaire', 'nom_complet' ]

    def get_nom_complet(self, obj):
        nom = (obj.nom_eleveur or "").upper()
        prenom = obj.prenom_eleveur or ""
        return f"{nom} {prenom}".strip()
        
class TypeDExploitantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeDExploitant
        fields = [ 'id_type_exploitant', 'description' ]
    

class ExploitantSerializer(serializers.ModelSerializer):
    membres = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    membres_ids = serializers.SerializerMethodField(read_only=True)

    type_exploitant = serializers.PrimaryKeyRelatedField(
        queryset = TypeDExploitant.objects.all(), allow_null = True
    )
    type_exploitant_detail = TypeDExploitantSerializer(source='type_exploitant', read_only=True)

    president = serializers.PrimaryKeyRelatedField(
        queryset = Eleveur.objects.all(), allow_null = True
    )

    class Meta:
        model = Exploitant
        read_only_fields = ['id_exploitant']
        fields = ['id_exploitant', 'nom_exploitant', 'president', 'membres', 'membres_ids', 'type_exploitant', 'type_exploitant_detail']

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
        # instance.type = validated_data.get('type', instance.type)
        instance.president = validated_data.get('president', instance.president)
        instance.type_exploitant = validated_data.get('type_exploitant', instance.type_exploitant)
        
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
    
    exploitant = serializers.PrimaryKeyRelatedField(
        queryset = Exploitant.objects.all(),
        allow_null = True
    )
    exploitant_detail = ExploitantSerializer(
        source='exploitant',
        read_only = True,
    )
    
    class Meta:
        model = SubventionPNV
        fields = [ 'id_subvention', 'description', 'montant', 'engage', 'paye', 'exploitant', 'exploitant_detail' ]

class LogementSerializer(GeoFeatureModelSerializer):
    unite_pastorale = serializers.PrimaryKeyRelatedField(
        queryset = UnitePastorale.objects.all(),
        allow_null = True
    )
    unite_pastorale_detail = UnitePastoraleLSerializer(
        source='unite_pastorale',
        read_only=True,
    )

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



class AbriDUrgenceCommoditeSerializer(serializers.ModelSerializer):
    abri_urgence_description = serializers.CharField(source='abri_urgence.description', read_only=True)
    commodite_desc = serializers.CharField(source='commodite.description', read_only=True)
    
    class Meta:
        model = AbriDUrgenceCommodite
        fields = [ 'id_abri_urgence_commodite', 'abri_urgence', 'commodite', 'etat', 'commentaire', 'quantite', 'abri_urgence_description', 'commodite_desc' ]
        



class BeneficierDeSerializer(GeoFeatureModelSerializer):
    
    exploitant_nom = serializers.SerializerMethodField() # CharField(source='exploitant.nom_exploitant', read_only=True)
    abri_description = serializers.SerializerMethodField() #CharField(source='abri_urgence.description', read_only=True)

    def get_exploitant_nom(self, obj):
        return obj.exploitant.nom_exploitant if obj.exploitant else None
    
    def get_abri_description(self, obj):
        return obj.abri_urgence.description if obj.abri_urgence else None
    
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
        fields = [ 'id_type_cheptel', 'description', 'espece', 'race', 'production', 'stade_maturite' ]

class EleverSerializer(serializers.ModelSerializer):
    # Année
    annee = serializers.SerializerMethodField()

    # Eleveur
    eleveur = serializers.PrimaryKeyRelatedField(
        queryset = Eleveur.objects.all(),
        allow_null = True,
    )
    eleveur_detail = EleveurSerializer(
        source='eleveur',
        read_only=True,
    )
    # Type de cheptel
    type_cheptel = serializers.PrimaryKeyRelatedField(
        queryset = TypeCheptel.objects.all(),
        allow_null = True,
    )
    type_cheptel_detail = TypeCheptelSerializer(
        source='type_cheptel',
        read_only=True,
    )
    # Situation d'exploitation
    situation_exploitation = serializers.PrimaryKeyRelatedField(
        queryset = SituationDExploitation.objects.all(),
        allow_null = True,
    )
    situation_detail = SituationDExploitationSerializer(
        source='situation_exploitation',
        read_only=True
    )
    
    class Meta:
        model = Elever
        fields = [ 'id_elever', 'date_debut', 'annee', 'date_fin', 'nombre_animaux', 'type_cheptel', 'type_cheptel_detail', 'eleveur', 'eleveur_detail',
                  'situation_exploitation', 'situation_detail' ]
    
    def get_annee(self, obj):
        if obj.date_debut:
            return obj.date_debut.year
        return None


##################
# Mise à jour Cheptels / types de cheptel
# le 9/2/26
class ProductionSerializer(serializers.ModelSerializer):
    """
    Production
    """

    class Meta:
        model = Production
        fields = [ 'id_production', 'description' ]

class Categorie_pensionSerializer(serializers.ModelSerializer):
    """
    Catégorie de pension
    """
    
    class Meta:
        model = Categorie_pension
        fields = [ 'id_categorie_pension', 'description' ]

class EspeceSerializer(serializers.ModelSerializer):
    """
    Espèce
    """
    
    class Meta:
        model = Espece
        fields = [ 'id_espece', 'description' ]

class RaceSerializer(serializers.ModelSerializer):
    """
    Race
    """

    class Meta:
        model = Race
        fields = [ 'id_race', 'description', 'espece' ]

class Categorie_animauxSerializer(serializers.ModelSerializer):
    """
    Catégorie d'animaux
    """
    
    class Meta:
        model = Categorie_animaux
        fields = [ 'id_categorie_animaux', 'description', 'espece' ]

class Type_cheptelSerializer(serializers.ModelSerializer):
    """
    Type de cheptel
    """
    
    class Meta:
        model = Type_cheptel
        fields = [ 'id_type_cheptel', 'description', 'production', 'pension', 'race', 'categorie_animaux' ]
        
class CheptelSerializer(serializers.ModelSerializer):
    """
    Cheptel
    """
    # Année
    annee = serializers.SerializerMethodField()

    # Eleveur
    eleveur = serializers.PrimaryKeyRelatedField(
        queryset = Eleveur.objects.all(),
        allow_null = True,
    )
    eleveur_detail = EleveurSerializer(
        source='eleveur',
        read_only=True,
    )
    
    # Type de cheptel
    type_cheptel = serializers.PrimaryKeyRelatedField(
        queryset = Type_cheptel.objects.all(),
        allow_null = True,
    )
    type_cheptel_detail = Type_cheptelSerializer(
        source='type_cheptel',
        read_only=True,
    )
    # Situation d'exploitation
    situation_exploitation = serializers.PrimaryKeyRelatedField(
        queryset = SituationDExploitation.objects.all(),
        allow_null = True,
    )
    situation_detail = SituationDExploitationSerializer(
        source='situation_exploitation',
        read_only=True
    )    

    class Meta:
        model = Cheptel
        fields = [ 'id_cheptel', 'date_debut', 'annee', 'date_fin', 'nombre_animaux', 'type_cheptel', 'type_cheptel_detail', 'eleveur', 'eleveur_detail', 
                  'situation_exploitation', 'situation_detail', 'description' ]

    def get_annee(self, obj):
        if obj.date_debut:
            return obj.date_debut.year
        return None

# FIN Mise à jour Cheptels / types de cheptel
##################



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

    def _find_unite_pastorale(self, geometry):
        # Rechercher l'unité pastorale qui contient la géométrie de l'événement

        if not geometry:
            return None
        
        if geometry.srid != 2154:
            geometry.transform(2154)

        # 1 - contains : la géométrie de l'événement est entièrement contenue dans l'unité pastorale
        up = UnitePastorale.objects.filter(
                                        geometry__contains=geometry,
                                        version_active=True,
                                    ).first()
        
        if up:
            return up
        
        # 2 - intersects : la géométrie de l'événement intersecte l'unité pastorale (bordures inclues)
        up = UnitePastorale.objects.filter(
                                        geometry__intersects=geometry,
                                        version_active=True,
                                    ).first()
        
        if up:
            return up
        
        # 3 - nearest : l'unité pastorale la plus proche de la géométrie de l'événement
        up = UnitePastorale.objects.filter(version_active=True).annotate(
                                        dist=Distance('geometry', geometry)
                                    ).order_by('dist').first()
        
        if up and up.dist and up.dist.m <= 50:  # Seuil de distance de 50 mètres pour associer l'événement à une unité pastorale:
            return up

        return None
    #----------
    # CREATE
    #----------
    def create(self, validated_data):
        geometry = validated_data.get('geometry', None)
        if geometry:
            validated_data['unite_pastorale'] = self._find_unite_pastorale(geometry)
        
        return super().create(validated_data)
    
    #----------
    # UPDATE
    #----------
    def update(self, instance, validated_data):
        new_geometry = validated_data.get('geometry', None)
        if new_geometry:
            if (not instance.geometry) or (instance.geometry.wkt != new_geometry.wkt):
                instance.unite_pastorale = self._find_unite_pastorale(new_geometry)
        
        return super().update(instance, validated_data)

    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)


class TypeEquipementSerializer(serializers.ModelSerializer):    
    class Meta:
        model = TypeEquipement
        fields = [ 'id_type_equipement', 'description', 'categorie' ]



class EquipementAlpageSerializer(GeoFeatureModelSerializer):
    type_equipement = serializers.PrimaryKeyRelatedField(
        queryset = TypeEquipement.objects.all(),
        allow_null = True,
    )
    type_equipement_detail = TypeEquipementSerializer(
        source='type_equipement',
        read_only=True
        )
    unite_pastorale = serializers.PrimaryKeyRelatedField(
        queryset = UnitePastorale.objects.all(),
        allow_null = True,
    )
    unite_pastorale_detail = UnitePastoraleLSerializer(
        source='unite_pastorale',
        read_only=True
    )

    class Meta:
        model = EquipementAlpage
        geo_field = 'geometry'
        auto_bbox = True
        fields = '__all__'
    
    def to_representation(self, instance):
        if (instance.geometry != None):
            instance.geometry.transform(4326)
        
        return super().to_representation(instance)
    
class EquipementExploitantSerializer(GeoFeatureModelSerializer):
    type_equipement = serializers.PrimaryKeyRelatedField(
        queryset = TypeEquipement.objects.all(),
        allow_null = True,
    )
    type_equipement_detail = TypeEquipementSerializer(
        source='type_equipement',
        read_only=True
        )
    unite_pastorale = serializers.PrimaryKeyRelatedField(
        queryset = UnitePastorale.objects.all(),
        allow_null = True,
    )
    unite_pastorale_detail = UnitePastoraleLSerializer(
        source='unite_pastorale',
        read_only=True
    )

    class Meta:
        model = EquipementExploitant
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