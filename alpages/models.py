from django.contrib.gis.db import models
from .choices_logement import LST_STATUT, LST_ACCES_FINAL, LST_PROPRIETE, LST_TYPE_LOGEMENT, LST_MULTIUSAGE, \
                              LST_ACTIVITE_LAITIERE, LST_ETAT_BATIMENT, LST_ACCUEIL_PUBLIC, LST_SURFACE_LOGEMENT, \
                              LST_WC, LST_ALIM_ELECTRIQUE, LST_ALIM_EAU, LST_ORIGINE_EAU, LST_QUALITE_EAU, \
                              LST_DISPO_EAU, LST_ASSAINISSEMENT, LST_CHAUFFE_EAU, LST_OUI_NON, LST_OUI_NON_INC

# Bloc administratif (orange)
class UnitePastorale(models.Model):
    """
    Unité pastorale
    """

    id_unite_pastorale = models.BigIntegerField(primary_key=True)  
    code_up = models.CharField(max_length=50, null=False, blank=False)
    nom_up = models.CharField(max_length=50, null=False, blank=False)
    annee_version = models. BigIntegerField(null=False, blank=False)
    geometry = models.MultiPolygonField(srid=2154, null=False, blank=False)
    version_active = models.BooleanField(null=False, blank=False)
    # proprietaire = models.ForeignKey('alpages.ProprietaireFoncier', on_delete=models.SET_NULL, blank=True, null=True, related_name='unites_pastorales')
    
    def __str__(self):
        return str(self.nom_up)
    
class ProprietaireFoncier(models.Model):
    """
    Proprétaire foncier
    """

    id_proprietaire = models.BigIntegerField(primary_key=True)  
    nom_propr = models.CharField(max_length=50, null=False, blank=False)
    prenom_propr = models.CharField(max_length=50, null=True, blank=True)
    tel_propr = models. CharField(max_length=30, null=True, blank=True)
    mail_propr = models.CharField(max_length=50, null=True, blank=True)
    adresse_propr = models.CharField(max_length=100, null=True, blank=True)
    commentaire = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return str(self.nom_propr)
    
# UP_Proprietaire = (#id_unite_pastorale, #id_proprietaire);
class UPProprietaire(models.Model):
    """
    Association Unité pastorale / Propriétaire foncier
    """
    
    id_up_proprietaire = models.BigIntegerField(primary_key=True)  
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='proprietaires')
    proprietaire = models.ForeignKey('alpages.ProprietaireFoncier', on_delete=models.SET_NULL, blank=True, null=True, related_name='unites_pastorales')
    
    def __str__(self):
        return f"{self.proprietaire} est propriétaire de {self.unite_pastorale}"
    
class QuartierPasto(models.Model):
    """
    Quartier d'alpage
    """

    id_quartier = models.BigIntegerField(primary_key=True)  
    code_quartier = models.CharField(max_length=50, null=True, blank=True)
    nom_quartier = models.CharField(max_length=50, null=True, blank=True)
    geometry = models.PolygonField(srid=2154, null=True, blank=True)
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='quartiers')
    
    def __str__(self):
        return str(self.nom_quartier)
    

# Bloc plans de suivi (bleu)
class TypeDeSuivi(models.Model):
    """
    Type de Suivi
    """

    id_type_suivi = models.BigIntegerField(primary_key=True)  
    description = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return str(self.description)

class PlanDeSuivi(models.Model):
    """
    Plan de Suivi
    """

    id_plan_suivi = models.BigIntegerField(primary_key=True)  
    description = models.CharField(max_length=50, null=False, blank=False)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    type_suivi = models.ForeignKey('alpages.TypeDeSuivi', on_delete=models.SET_NULL, blank=True, null=True, related_name='plans_de_suivi')
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='plans_de_suivi')
    
    def __str__(self):
        return str(self.description)
    
# Type_de_mesure
class TypeDeMesure(models.Model):
    """
    Type de mesure
    """

    id_type_mesure = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return str(self.description)


# Mesure_de_plan
class MesureDePlan(models.Model):
    """
    Mesure de plan
    """

    id_mesure_plan = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    commentaire = models.CharField(max_length=50, null=True, blank=True)
    debut_periode = models.DateField(null=True, blank=True)
    fin_periode = models.DateField(null=True, blank=True)
    # geometry = models.TextField(null=True, blank=True)
    type_mesure = models.ForeignKey('alpages.TypeDeMesure', on_delete=models.SET_NULL, blank=True, null=True, related_name='mesures_de_plan')
    plan_suivi = models.ForeignKey('alpages.PlanDeSuivi', on_delete=models.SET_NULL, blank=True, null=True, related_name='mesures_de_plan')

    def __str__(self):
        return str(self.description)


# Bloc exploitation
class TypeConvention(models.Model):
    """
    Type de convention
    """
    
    id_type_convention = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return str(self.description)


class ConventionDExploitation(models.Model):
    """
    Convention d'exploitation
    """
    
    id_convention = models.BigIntegerField(primary_key=True)
    surface_location = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    surface_exploitable = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    effectif_bovin = models.IntegerField(null=True, blank=True)
    effectif_ovin = models.IntegerField(null=True, blank=True)
    effectif_caprin = models.IntegerField(null=True, blank=True)
    effectif_porcin = models.IntegerField(null=True, blank=True)
    debut_periode_expl = models.DateField(null=True, blank=True)
    fin_periode_expl = models.DateField(null=True, blank=True)
    geometry = models.PolygonField(srid=2154, null=True, blank=True)
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='conventions')
    exploitant = models.ForeignKey('alpages.Exploitant', on_delete=models.SET_NULL, blank=True, null=True, related_name='conventions')
    type_convention = models.ForeignKey('alpages.TypeConvention', on_delete=models.SET_NULL, blank=True, null=True, related_name='conventions')
    
    def __str__(self):
        return str(self.id_convention)
    

class SituationDExploitation(models.Model):
    """
    Situation d'exploitation
    """
    
    id_situation = models.BigIntegerField(primary_key=True)
    nom_situation = models.CharField(max_length=50, null=False, blank=False)
    situation_active = models.BooleanField(null=False, blank=False)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='situations')
    exploitant = models.ForeignKey('alpages.Exploitant', on_delete=models.SET_NULL, blank=True, null=True, related_name='situations')
    
    def __str__(self):
        return str(self.nom_situation)

# Exploiter = (#id_quartier, #id_situation, date_debut DATE, date_fin DATE, commmentaire VARCHAR(500));
class Exploiter(models.Model):
    """
    Exploiter
    """
    
    id_exploiter = models.BigIntegerField(primary_key=True)
    quartier = models.ForeignKey('alpages.QuartierPasto', on_delete=models.SET_NULL, blank=True, null=True, related_name='exploitations')
    situation_exploitation = models.ForeignKey('alpages.SituationDExploitation', on_delete=models.SET_NULL, blank=True, null=True, related_name='exploitations')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    commentaire = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return f"{self.situation} exploite {self.quartier}"


class Eleveur(models.Model):
    """
    Eleveur
    """
    
    id_eleveur = models.BigIntegerField(primary_key=True)
    nom_eleveur = models.CharField(max_length=50, null=False, blank=False)
    prenom_eleveur = models.CharField(max_length=50, null=True, blank=True)
    tel_eleveur = models.CharField(max_length=50, null=True, blank=True)
    mail_eleveur = models.CharField(max_length=50, null=True, blank=True)
    adresse_eleveur = models.CharField(max_length=50, null=True, blank=True)
    commentaire = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.nom_eleveur)
    
class Exploitant(models.Model):
    """
    Exploitant
    """
    
    id_exploitant = models.BigIntegerField(primary_key=True)
    nom_exploitant = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=50, null=True, blank=True)
    president = models.ForeignKey('alpages.Eleveur', on_delete=models.SET_NULL, blank=True, null=True, related_name='exploitants')
    
    def __str__(self):
        return str(self.nom_exploitant)

class EtreCompose(models.Model):
    """
    EtreCompose (association exploitant / éleveurs)
    """
    exploitant = models.ForeignKey(Exploitant, on_delete=models.SET_NULL, blank=True, null=True, )
    eleveur = models.ForeignKey(Eleveur, on_delete=models.SET_NULL, blank=True, null=True, )

    class Meta:
        unique_together = ('exploitant', 'eleveur')
    
    def __str__(self):
        return f"{self.eleveur} est membre de {self.exploitant}"
    
class SubventionPNV(models.Model):
    """
    Subvention PNV
    """
    
    id_subvention = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    montant = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False)
    engage = models.BooleanField(null=False, blank=False, default=False)
    paye = models.BooleanField(null=False, blank=False, default=False)
    exploitant = models.ForeignKey('alpages.Exploitant', on_delete=models.SET_NULL, blank=True, null=True, related_name='subventions')
    
    def __str__(self):
        return str(self.description)

class Logement(models.Model):
    """
    Classe Logement
    Champs et valeurs issues des échanges avec la SEA73
    """
    
    logement_code = models.CharField(max_length=10)
    statut = models.CharField(max_length=50, choices=LST_STATUT, null=True, blank=True)
    acces_final = models.CharField(max_length=50, choices=LST_ACCES_FINAL, null=True, blank=True)
    propriete = models.CharField(max_length=50, choices=LST_PROPRIETE, null=True, blank=True)
    type_logement = models.CharField(max_length=50, choices=LST_TYPE_LOGEMENT, null=True, blank=True)
    multiusage = models.CharField(max_length=50, choices=LST_MULTIUSAGE, null=True, blank=True)
    activite_laitiere = models.CharField(max_length=50, choices=LST_ACTIVITE_LAITIERE, null=True, blank=True)
    etat_batiment = models.CharField(max_length=50, choices=LST_ETAT_BATIMENT, null=True, blank=True)
    accueil_public = models.CharField(max_length=50, choices=LST_ACCUEIL_PUBLIC, null=True, blank=True)
    mixite_possible = models.CharField(max_length=50, choices=LST_OUI_NON_INC, null=True, blank=True)
    surface_logement = models.CharField(max_length=50, choices=LST_SURFACE_LOGEMENT, null=True, blank=True)
    presence_douche = models.CharField(max_length=50, choices=LST_OUI_NON_INC, null=True, blank=True)
    type_wc = models.CharField(max_length=50, choices=LST_WC, null=True, blank=True)
    alim_elec = models.CharField(max_length=50, choices=LST_ALIM_ELECTRIQUE, null=True, blank=True)
    alim_eau = models.CharField(max_length=50, choices=LST_ALIM_EAU, null=True, blank=True)
    origine_eau = models.CharField(max_length=50, choices=LST_ORIGINE_EAU, null=True, blank=True)
    qualite_eau = models.CharField(max_length=50, choices=LST_QUALITE_EAU, null=True, blank=True)
    dispo_eau = models.CharField(max_length=50, choices=LST_DISPO_EAU, null=True, blank=True)
    assainissement = models.CharField(max_length=50, choices=LST_ASSAINISSEMENT, null=True, blank=True)
    chauffe_eau = models.CharField(max_length=50, choices=LST_CHAUFFE_EAU, null=True, blank=True)
    chauffage = models.CharField(max_length=50, choices=LST_OUI_NON, null=True, blank=True)
    stockage_indep = models.CharField(max_length=50, choices=LST_OUI_NON, null=True, blank=True)
    
    geom = models.PointField(srid=2154, null=True)


class Commodite(models.Model):
    """
    Commodite
    """
    
    id_commodite = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return str(self.description)
    

class LogementCommodite(models.Model):
    """
    Association Logement / Commodite
    """
    
    id_logement_commodite = models.BigIntegerField(primary_key=True)
    logement = models.ForeignKey('alpages.Logement', on_delete=models.SET_NULL, blank=True, null=True, related_name='commodites')
    commodite = models.ForeignKey('alpages.Commodite', on_delete=models.SET_NULL, blank=True, null=True, related_name='logements')
    etat = models.CharField(max_length=50, null=False, blank=False)
    commentaire = models.CharField(max_length=50, null=True, blank=True)
    quantite = models.CharField(max_length=50, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.logement} a {self.quantite} de {self.commodite}"


class AbriDUrgence(models.Model):
    """
    Abri d'urgence
    """
    
    id_abri_urgence = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    etat = models.CharField(max_length=50, null=False, blank=False)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=50, null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return str(self.description)

class BeneficierDe(models.Model):
    """
    Association Exploitant / Abri d'urgence
    """
    
    id_beneficier_de = models.BigIntegerField(primary_key=True)  
    exploitant = models.ForeignKey('alpages.Exploitant', on_delete=models.SET_NULL, blank=True, null=True, related_name='beneficiaires')
    abri_urgence = models.ForeignKey('alpages.AbriDUrgence', on_delete=models.SET_NULL, blank=True, null=True, related_name='beneficiaires')
    date_debut = models.DateField(null=False, blank=False)
    date_fin = models.DateField(null=True, blank=True)
    geometry = models.PointField(srid=2154, null=True, blank=True)
    
    def __str__(self):
        return f"{self.exploitant} bénéficie de {self.abri_urgence}"
    
# Ruche / Berger / Type Cheptel
class Ruche(models.Model):
    """
    Ruche
    """
    
    id_ruche = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    geometry = models.PointField(srid=2154, null=False, blank=False)
    situation_exploitation = models.ForeignKey('alpages.SituationDExploitation', on_delete=models.SET_NULL, blank=True, null=True, related_name='ruches')
    
    def __str__(self):
        return str(self.description)

class Berger(models.Model):
    """
    Berger
    """
    
    id_berger = models.BigIntegerField(primary_key=True)
    nom_berger = models.CharField(max_length=50, null=False, blank=False)
    prenom_berger = models.CharField(max_length=50, null=False, blank=False)
    tel_berger = models.CharField(max_length=50, null=True, blank=True)
    adresse_berger = models.CharField(max_length=50, null=True, blank=True)
    commentaire = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.nom_berger)

class GardeSituation(models.Model):
    """
    Garde situation
    """
    
    id_garde_situation = models.BigIntegerField(primary_key=True)
    date_debut = models.DateField(null=False, blank=False)
    date_fin = models.DateField(null=True, blank=True)
    commentaire = models.CharField(max_length=500, null=True, blank=True)
    situation_exploitation = models.ForeignKey('alpages.SituationDExploitation', on_delete=models.SET_NULL, blank=True, null=True, related_name='gardes_situation')
    berger = models.ForeignKey('alpages.Berger', on_delete=models.SET_NULL, blank=True, null=True, related_name='gardes_situation')
    
    def __str__(self):
        return str(self.id_garde_situation)

class TypeCheptel(models.Model):
    """
    Type de cheptel
    """
    
    id_type_cheptel = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    espece = models.CharField(max_length=50, null=False, blank=False)
    race = models.CharField(max_length=50, null=True, blank=True)
    production = models.CharField(max_length=50, null=True, blank=True)
    stade_maturite = models.CharField(max_length=50, null=True, blank=True)
    pension = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.description)

class Elever(models.Model):
    """
    Association Eleveur / Cheptel
    """
    
    id_elever = models.BigIntegerField(primary_key=True)
    situation_exploitation = models.ForeignKey('alpages.SituationDExploitation', on_delete=models.SET_NULL, blank=True, null=True, related_name='eleveurs')
    type_cheptel = models.ForeignKey('alpages.TypeCheptel', on_delete=models.SET_NULL, blank=True, null=True, related_name='eleveurs')
    eleveur = models.ForeignKey('alpages.Eleveur', on_delete=models.SET_NULL, blank=True, null=True, related_name='eleveurs')
    nombre_animaux = models.IntegerField(null=False, blank=False)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.eleveur} élève {self.type_cheptel} dans la situation {self.situation_exploitation}"
    
# Evénements
class TypeEvenement(models.Model):
    """
    Type d'événement
    """
    
    id_type_evenement = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return str(self.description)

class Evenement(models.Model):
    """
    Evenement
    """
    
    id_evenement = models.BigIntegerField(primary_key=True)
    date_evenement = models.DateField(null=False, blank=False)
    observateur = models.CharField(max_length=50, null=False, blank=False)
    date_observation = models.DateField(null=False, blank=False)
    source = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    geometry = models.GeometryField(srid=2154, null=True, blank=True)
    # equipement_exploitant = models.ForeignKey('alpages.EquipementExploitant', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    # situation = models.ForeignKey('alpages.SituationDExploitation', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    mesure_plan = models.ForeignKey('alpages.MesureDePlan', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    # logement = models.ForeignKey('alpages.Logement', on_delete=models.CASCADE, related_name='evenements')
    # equipement_alpage = models.ForeignKey('alpages.EquipementAlpage', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    unite_pastorale = models.ForeignKey('alpages.UnitePastorale', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    type_evenement = models.ForeignKey('alpages.TypeEvenement', on_delete=models.SET_NULL, blank=True, null=True, related_name='evenements')
    
    def __str__(self):
        return str(self.description)


# TEMPORAIRE DLG
class Quartieralpage(models.Model):
    """
    Quartier d'alpage
    """

    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=2154, blank=True, null=True)
    quartier_code_court = models.CharField(max_length=10, blank=True, null=True)
    date_presence_troupeau = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alpages_quartieralpage'
        
class QuartierUP(models.Model):
    """
    Quartier d'alpages
    """
    
    quartier_code = models.CharField(max_length=15, null=True, blank=True)
    surface = models.FloatField(null=True, blank=True)
    up_code = models.CharField(max_length=254, null=True, blank=True)
    up_nom_1 = models.CharField(max_length=254, null=True, blank=True)
    up_nom_2 = models.CharField(max_length=254, null=True, blank=True)
    quartier_code_court = models.CharField(max_length=254, null=True, blank=True)
    quartier_nom = models.CharField(max_length=254, null=True, blank=True)
    
    geom = models.MultiPolygonField(srid=2154, null=True)

    def __str__(self):
        return str(self.quartier_code)


# TEST CC
class LogementTest(models.Model):
    """
    Test logement
    """
    id_logement_test = models.BigIntegerField(primary_key=True)
    nom_logement_test = models.CharField(max_length=254)
 
    geometry = models.PointField(srid=2154, blank=True, null=True)

    def __str__(self):
        return str(self.nom_logement_test)

