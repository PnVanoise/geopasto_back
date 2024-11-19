LST_STATUT = [
    ('existant', 'existant'),
    ('besoin', 'besoin')
]

LST_ACCES_FINAL = [
    ('carrossable', 'carrossable'),
    ('4_4', '4*4'),
    ('quad', 'quad'),
    ('pedestre', 'pédestre')
]

LST_PROPRIETE = [
    ('communal', 'communal'),
    ('domanial', 'domanial'),
    ('prive', 'privé'),
    ('afp', 'afp'),
    ('gp', 'gp'),
    ('departemental', 'départemental'),
    ('domaine_skiable', 'domaine skiable'),
    ('autre collectivité', 'autre collectivité')
]

LST_TYPE_LOGEMENT = [
    ('logement_principal', 'logement principal'),
    ('logement_secondaire', 'logement secondaire'),
    ('abri_sommaire', 'abri sommaire')
]

LST_MULTIUSAGE = [
    ('uniquement_pastoral', 'uniquement pastoral'),
    ('abri_randonneurs', 'abri randonneurs'),
    ('refuge_garde', 'refuge gardé'),
    ('resto_station_ski', 'resto station ski'),
    ('poste_de_secours', 'poste de secours'),
    ('autre', 'autre')
]

LST_ACCUEIL_PUBLIC = [
    ('aucun_accueil', 'aucun accueil du public'),
    ('accueil_ss_vente', 'accueil du public sans vente'),
    ('accueil_vente', 'accueil et vente au public'),
    ('vente_ss_accueil', 'vente sans accueil du public')
]

LST_SURFACE_LOGEMENT = [
    ('inf14', '< 14 m2'),
    ('sup14_inf20', '[14 - 20] m2'),
    ('sup20_inf40', ']20 - 40] m2'),
    ('sup40_inf80', ']40 - 80] m2'),
    ('sup80', '> 80 m2'),
]

LST_WC = [
    ('toilettes_seches', 'toilettes sèches'),
    ('classique', 'classique'),
    ('absence', 'absence'),
    ('inconnu', 'inconnu')
]

LST_ALIM_ELECTRIQUE = [
    ('mini_renouv', 'mini renouvelable'),
    ('renouv_inter', 'renouvelable intermédiaire'),
    ('gros_renouv', 'gros renouvelable'),
    ('reseau_public', 'réseau public'),
    ('groupe_elec', 'groupe électrogène'),
    ('absence', 'absence')
]

LST_ALIM_EAU = [
    ('interieur', 'intérieur'),
    ('ext_inf50', 'extérieur < 50m'),
    ('ext_sup50', 'extérieur > 50 m'),
    ('absence', 'absence')
]

LST_ORIGINE_EAU = [
    ('source_captee', 'source captée'),
    ('eau_de_surface', 'eau de surface'),
    ('impluvium', 'impluvium'),
    ('recup_toiture', 'récupération toiture'),
    ('reseau', 'réseau'),
    ('transport', 'transport'),
    ('absence', 'absence')
]

LST_QUALITE_EAU = [
    ('non_consommee', 'non consommée'),
    ('eau_consommee', 'eau consommée'),
    ('eau_traitee', 'eau traitée'),
    ('eau_regl_potable', 'eau réglementairement potable'),
]

LST_DISPO_EAU = [
    ('a_volonte', 'à volonté'),
    ('irregulier', 'irrégulier'),
    ('absence', 'absence'),
    ('inconnnu', 'inconnu')
]

LST_ASSAINISSEMENT = [
    ('puits_perdu', 'puits perdu'),
    ('fosse_septique', 'fosse septique'),
    ('tout à l\'égoût', 'tout à l\'égoût'),
    ('bassin_trt', 'bassin de traitement'),
    ('champ_epandage', 'champ d\'épandage'),
    ('absence', 'absence')
]

LST_CHAUFFE_EAU = [
    ('chauffe_eau_gaz', 'chauffe-eau gaz'),
    ('chauffe_eau_elec', 'chauffe-eau électrique'),
    ('poele_bois', 'poêle bouilleur au bois'),
    ('chauffe_eau_solaire', 'chauffe-eau solaire'),
    ('absence', 'absence')
]


LST_ACTIVITE_LAITIERE = [
    ('salle_de_traite', 'salle de traite'),
    ('salle_de_transformation', 'salle de transformation'),
    ('les_deux', 'les deux'),
    ('aucune', 'aucune'),
    ('inconnu', 'inconnu')
]

LST_ETAT_BATIMENT = [
    ('bon', 'bon'),
    ('moyen', 'moyen'),
    ('delabre', 'délabré')
]

LST_OUI_NON = [
    ('oui', 'oui'),
    ('non', 'non')
]

LST_OUI_NON_INC = [
    ('oui', 'oui'),
    ('non', 'non'),
    ('inconnu', 'inconnu')
]