"""
Comprehensive serializer tests for the alpages app.

Existing smoke tests (SerializersSmokeTest) are preserved unchanged.
All new tests use IDs >= 100 to avoid conflicts with the smoke-test IDs (20, 21).

GeoFeature serializers (QuartierPasto, BeneficierDe) expose non-geometry fields
under data['properties'] and the geometry under data['geometry'].
"""

from datetime import date
from decimal import Decimal

from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from alpages.models import (
    UnitePastorale, ProprietaireFoncier, UPProprietaire, QuartierPasto,
    TypeDeSuivi, PlanDeSuivi, TypeDeMesure, MesureDePlan,
    TypeConvention, SituationDExploitation, Exploiter,
    Eleveur, TypeDExploitant, Exploitant, EtreCompose, SubventionPNV,
    Logement, Commodite, LogementCommodite,
    AbriDUrgence, AbriDUrgenceCommodite, BeneficierDe,
    Berger, GardeSituation, TypeCheptel, Elever,
    Production, Categorie_pension, Espece, Race, Categorie_animaux,
    Cheptel, Type_cheptel,
    TypeEvenement, TypeEquipement,
)
from alpages.serializers import (
    EleveurSerializer, SituationDExploitationSerializer,
    ExploiterSerializer, UPProprietaireSerializer,
    QuartierPastoSerializer, GardeSituationSerializer,
    EleverSerializer, ExploitantSerializer,
    BeneficierDeSerializer, PlanDeSuiviSerializer, MesureDePlanSerializer,
    SubventionPNVSerializer, LogementCommoditeSerializer,
    TypeConventionSerializer, TypeDeSuiviSerializer, TypeDeMesureSerializer,
    BergerSerializer, TypeCheptelSerializer, ProductionSerializer,
    Categorie_pensionSerializer, EspeceSerializer, RaceSerializer,
    Categorie_animauxSerializer, CheptelSerializer, Type_cheptelSerializer,
    TypeEvenementSerializer, TypeEquipementSerializer, AbriDUrgenceSerializer,
    CommoditeSerializer, AbriDUrgenceCommoditeSerializer,
)

# ---------------------------------------------------------------------------
# Geometry helpers (SRID 2154 - RGF93 / Lambert-93).
# Each call returns a brand-new GEOSGeometry instance so that the in place
# transform() calls made by GeoFeature serializers do not affect other tests.
# ---------------------------------------------------------------------------

def _up_geom():
    return GEOSGeometry('SRID=2154;MULTIPOLYGON(((0 0,0 1,1 1,1 0,0 0)))')


def _qp_geom():
    return GEOSGeometry('SRID=2154;POLYGON((0 0,0 1,1 1,1 0,0 0))')


def _pt_geom():
    return GEOSGeometry('SRID=2154;POINT(0 0)')


# ============================================================================
# Original smoke tests (MUST NOT be changed)
# ============================================================================

class SerializersSmokeTest(TestCase):

    def test_situation_serializer_fields(self):
        s = SituationDExploitation.objects.create(id_situation=20, nom_situation='S20', situation_active=True, date_debut=date(2020,1,1))
        ser = SituationDExploitationSerializer(s)
        data = ser.data
        self.assertIn('id_situation', data)
        self.assertIn('nom_situation', data)

    def test_commodite_serializer(self):
        c = Commodite.objects.create(id_commodite=20, description='C20')
        ser = CommoditeSerializer(c)
        self.assertEqual(ser.data['description'], 'C20')

    def test_abri_commodite_serializer(self):
        a = AbriDUrgence.objects.create(id_abri_urgence=20, description='A20', etat='OK')
        c = Commodite.objects.create(id_commodite=21, description='C21')
        ac = AbriDUrgenceCommodite.objects.create(id_abri_urgence_commodite=20, abri_urgence=a, commodite=c, etat='OK')
        ser = AbriDUrgenceCommoditeSerializer(ac)
        self.assertIn('abri_urgence_description', ser.data)
        self.assertIn('commodite_desc', ser.data)


# ============================================================================
# EleveurSerializer
# ============================================================================

class EleveurSerializerTest(TestCase):
    """Tests for EleveurSerializer, focusing on the nom_complet computed field."""

    def test_nom_complet_with_nom_and_prenom(self):
        """nom='dupont', prenom='jean' → 'DUPONT jean'."""
        e = Eleveur.objects.create(id_eleveur=100, nom_eleveur='dupont', prenom_eleveur='jean')
        data = EleveurSerializer(e).data
        self.assertEqual(data['nom_complet'], 'DUPONT jean')

    def test_nom_complet_with_nom_only_prenom_none(self):
        """nom='martin', prenom=None → 'MARTIN' (trailing space stripped)."""
        e = Eleveur.objects.create(id_eleveur=101, nom_eleveur='martin', prenom_eleveur=None)
        data = EleveurSerializer(e).data
        self.assertEqual(data['nom_complet'], 'MARTIN')

    def test_nom_complet_with_empty_string_prenom(self):
        """nom='martin', prenom='' → 'MARTIN' (same as None case)."""
        e = Eleveur.objects.create(id_eleveur=102, nom_eleveur='martin', prenom_eleveur='')
        data = EleveurSerializer(e).data
        self.assertEqual(data['nom_complet'], 'MARTIN')

    def test_basic_field_presence(self):
        """All expected fields must be present in the serialized output."""
        e = Eleveur.objects.create(id_eleveur=103, nom_eleveur='Test')
        data = EleveurSerializer(e).data
        for field in ('id_eleveur', 'nom_eleveur', 'prenom_eleveur', 'nom_complet',
                      'adresse_eleveur', 'tel_eleveur', 'mail_eleveur', 'commentaire'):
            self.assertIn(field, data, msg=f"Missing field: {field}")


# ============================================================================
# SituationDExploitationSerializer – extended
# ============================================================================

class SituationDExploitationExtendedTest(TestCase):
    """Additional tests for the exploitant_nom computed field."""

    def test_exploitant_nom_when_exploitant_is_set(self):
        exploitant = Exploitant.objects.create(id_exploitant=100, nom_exploitant='Ferme100')
        sit = SituationDExploitation.objects.create(
            id_situation=100, nom_situation='S100',
            situation_active=True, exploitant=exploitant,
        )
        data = SituationDExploitationSerializer(sit).data
        self.assertEqual(data['exploitant_nom'], 'Ferme100')

    def test_exploitant_nom_is_none_when_no_exploitant(self):
        sit = SituationDExploitation.objects.create(
            id_situation=101, nom_situation='S101', situation_active=True,
        )
        data = SituationDExploitationSerializer(sit).data
        self.assertIsNone(data['exploitant_nom'])


# ============================================================================
# ExploiterSerializer
# ============================================================================

class ExploiterSerializerTest(TestCase):
    """Tests for the situation_nom and quartier_nom source-based fields."""

    def test_situation_nom_and_quartier_nom_populated_when_fks_set(self):
        up = UnitePastorale.objects.create(
            id_unite_pastorale=100, code_up='UP100', nom_up='UP Cent',
            annee_version=2024, geometry=_up_geom(), version_active=True,
        )
        qp = QuartierPasto.objects.create(
            id_quartier=100, nom_quartier='Quartier100',
            geometry=_qp_geom(), unite_pastorale=up,
        )
        sit = SituationDExploitation.objects.create(
            id_situation=102, nom_situation='Sit102', situation_active=True,
        )
        exp = Exploiter.objects.create(
            id_exploiter=100, quartier=qp, situation_exploitation=sit,
        )
        data = ExploiterSerializer(exp).data
        self.assertEqual(data['situation_nom'], 'Sit102')
        self.assertEqual(data['quartier_nom'], 'Quartier100')


# ============================================================================
# UPProprietaireSerializer
# ============================================================================

class UPProprietaireSerializerTest(TestCase):
    """Tests for the up_nom and proprietaire_nom source-based fields."""

    def test_up_nom_and_proprietaire_nom_populated(self):
        up = UnitePastorale.objects.create(
            id_unite_pastorale=101, code_up='UP101', nom_up='UP101 Nom',
            annee_version=2024, geometry=_up_geom(), version_active=True,
        )
        prop = ProprietaireFoncier.objects.create(
            id_proprietaire=100, nom_propr='DuBois',
        )
        upp = UPProprietaire.objects.create(
            id_up_proprietaire=100, unite_pastorale=up, proprietaire=prop,
        )
        data = UPProprietaireSerializer(upp).data
        self.assertEqual(data['up_nom'], 'UP101 Nom')
        self.assertEqual(data['proprietaire_nom'], 'DuBois')


# ============================================================================
# QuartierPastoSerializer  (GeoFeature – properties under data['properties'])
# ============================================================================

class QuartierPastoSerializerTest(TestCase):
    """
    QuartierPastoSerializer is a GeoFeatureModelSerializer.
    Non-geometry fields are nested under data['properties'].
    """

    def test_unitepastorale_nom_in_properties_when_up_set(self):
        up = UnitePastorale.objects.create(
            id_unite_pastorale=102, code_up='UP102', nom_up='UP102 Nom',
            annee_version=2024, geometry=_up_geom(), version_active=True,
        )
        qp = QuartierPasto.objects.create(
            id_quartier=101, nom_quartier='QP101',
            geometry=_qp_geom(), unite_pastorale=up,
        )
        data = QuartierPastoSerializer(qp).data
        self.assertEqual(data['properties']['unitepastorale_nom'], 'UP102 Nom')

    def test_unitepastorale_nom_is_none_when_no_up(self):
        qp = QuartierPasto.objects.create(
            id_quartier=102, nom_quartier='QP102',
            geometry=_qp_geom(), unite_pastorale=None,
        )
        data = QuartierPastoSerializer(qp).data
        self.assertIsNone(data['properties']['unitepastorale_nom'])

    def test_geometry_none_returns_empty_polygon_fallback(self):
        """When geometry is None the serializer substitutes an empty Polygon."""
        qp = QuartierPasto.objects.create(
            id_quartier=103, nom_quartier='QP103', geometry=None,
        )
        data = QuartierPastoSerializer(qp).data
        self.assertEqual(data['geometry'], {"type": "Polygon", "coordinates": [[]]})

    def test_geometry_set_returns_geojson_feature(self):
        """A QuartierPasto with a real geometry must be serialized as a GeoJSON Feature."""
        qp = QuartierPasto.objects.create(
            id_quartier=104, nom_quartier='QP104', geometry=_qp_geom(),
        )
        data = QuartierPastoSerializer(qp).data
        self.assertEqual(data['type'], 'Feature')


# ============================================================================
# GardeSituationSerializer
# ============================================================================

class GardeSituationSerializerTest(TestCase):
    """Tests for the berger_nom, berger_prenom, and situation_nom fields."""

    def test_berger_nom_prenom_and_situation_nom_populated(self):
        berger = Berger.objects.create(
            id_berger=100, nom_berger='Mouton', prenom_berger='Pierre',
        )
        sit = SituationDExploitation.objects.create(
            id_situation=103, nom_situation='Sit103', situation_active=True,
        )
        gs = GardeSituation.objects.create(
            id_garde_situation=100, date_debut=date(2023, 1, 1),
            berger=berger, situation_exploitation=sit,
        )
        data = GardeSituationSerializer(gs).data
        self.assertEqual(data['berger_nom'], 'Mouton')
        self.assertEqual(data['berger_prenom'], 'Pierre')
        self.assertEqual(data['situation_nom'], 'Sit103')


# ============================================================================
# EleverSerializer
# ============================================================================

class EleverSerializerTest(TestCase):
    """Tests for EleverSerializer, including the annee computed field and nested details."""

    # ------------------------------------------------------------------
    # Private helpers — each creates fresh objects for the test.
    # ------------------------------------------------------------------
    def _make_eleveur(self):
        return Eleveur.objects.create(id_eleveur=104, nom_eleveur='Berret')

    def _make_type_cheptel(self):
        return TypeCheptel.objects.create(id_type_cheptel=100, description='Bovin', espece='Bovins')

    def _make_situation(self):
        return SituationDExploitation.objects.create(
            id_situation=104, nom_situation='Sit104', situation_active=True,
        )

    # ------------------------------------------------------------------
    # annee
    # ------------------------------------------------------------------
    def test_annee_returns_year_when_date_debut_set(self):
        e = self._make_eleveur()
        el = Elever.objects.create(
            id_elever=100, eleveur=e, nombre_animaux=10, date_debut=date(2023, 6, 1),
        )
        self.assertEqual(EleverSerializer(el).data['annee'], 2023)

    def test_annee_returns_none_when_date_debut_is_none(self):
        e = self._make_eleveur()
        el = Elever.objects.create(id_elever=101, eleveur=e, nombre_animaux=5)
        self.assertIsNone(EleverSerializer(el).data['annee'])

    # ------------------------------------------------------------------
    # Nested detail fields
    # ------------------------------------------------------------------
    def test_eleveur_detail_contains_nom_eleveur(self):
        e = self._make_eleveur()
        el = Elever.objects.create(id_elever=102, eleveur=e, nombre_animaux=3)
        self.assertIn('nom_eleveur', EleverSerializer(el).data['eleveur_detail'])

    def test_type_cheptel_detail_contains_description(self):
        e = self._make_eleveur()
        tc = self._make_type_cheptel()
        el = Elever.objects.create(id_elever=103, eleveur=e, type_cheptel=tc, nombre_animaux=7)
        self.assertIn('description', EleverSerializer(el).data['type_cheptel_detail'])

    def test_situation_detail_contains_nom_situation(self):
        e = self._make_eleveur()
        sit = self._make_situation()
        el = Elever.objects.create(
            id_elever=104, eleveur=e, situation_exploitation=sit, nombre_animaux=2,
        )
        self.assertIn('nom_situation', EleverSerializer(el).data['situation_detail'])


# ============================================================================
# ExploitantSerializer
# ============================================================================

class ExploitantSerializerTest(TestCase):
    """Tests for ExploitantSerializer: membres_ids, create, and update logic."""

    def _make_eleveur(self, pk, nom):
        return Eleveur.objects.create(id_eleveur=pk, nom_eleveur=nom)

    def test_membres_ids_returns_list_of_eleveur_ids(self):
        exp = Exploitant.objects.create(id_exploitant=100, nom_exploitant='Groupement100')
        e1 = self._make_eleveur(105, 'E1')
        e2 = self._make_eleveur(106, 'E2')
        EtreCompose.objects.create(exploitant=exp, eleveur=e1)
        EtreCompose.objects.create(exploitant=exp, eleveur=e2)
        data = ExploitantSerializer(exp).data
        self.assertCountEqual(data['membres_ids'], [105, 106])

    def test_create_with_membres_creates_etre_compose_records(self):
        e = self._make_eleveur(107, 'EleveurCreate')
        ser = ExploitantSerializer(data={
            'id_exploitant': 101,
            'nom_exploitant': 'GroupCreate',
            'membres': [107],
            'president': None,
            'type_exploitant': None,
        })
        self.assertTrue(ser.is_valid(), ser.errors)
        instance = ser.save()
        self.assertTrue(
            EtreCompose.objects.filter(exploitant=instance, eleveur=e).exists(),
            "EtreCompose should be created for the provided member.",
        )

    def test_update_adds_new_and_removes_old_membres(self):
        exp = Exploitant.objects.create(id_exploitant=102, nom_exploitant='GroupUpdate')
        old_e = self._make_eleveur(108, 'OldMember')
        new_e = self._make_eleveur(109, 'NewMember')
        EtreCompose.objects.create(exploitant=exp, eleveur=old_e)

        ser = ExploitantSerializer(exp, data={
            'id_exploitant': 102,
            'nom_exploitant': 'GroupUpdate',
            'membres': [109],
            'president': None,
            'type_exploitant': None,
        })
        self.assertTrue(ser.is_valid(), ser.errors)
        ser.save()

        self.assertFalse(
            EtreCompose.objects.filter(exploitant=exp, eleveur=old_e).exists(),
            "Old member should have been removed.",
        )
        self.assertTrue(
            EtreCompose.objects.filter(exploitant=exp, eleveur=new_e).exists(),
            "New member should have been added.",
        )


# ============================================================================
# BeneficierDeSerializer  (GeoFeature – properties under data['properties'])
# ============================================================================

class BeneficierDeSerializerTest(TestCase):
    """
    BeneficierDeSerializer is a GeoFeatureModelSerializer.
    Computed fields exploitant_nom and abri_description live under data['properties'].
    """

    def test_exploitant_nom_and_abri_description_populated(self):
        exp = Exploitant.objects.create(id_exploitant=103, nom_exploitant='ExploitantBen')
        abri = AbriDUrgence.objects.create(
            id_abri_urgence=100, description='Abri100', etat='Bon',
        )
        bd = BeneficierDe.objects.create(
            id_beneficier_de=100, exploitant=exp, abri_urgence=abri,
            date_debut=date(2024, 1, 1), geometry=_pt_geom(),
        )
        data = BeneficierDeSerializer(bd).data
        self.assertEqual(data['properties']['exploitant_nom'], 'ExploitantBen')
        self.assertEqual(data['properties']['abri_description'], 'Abri100')

    def test_exploitant_nom_is_none_when_no_exploitant(self):
        bd = BeneficierDe.objects.create(
            id_beneficier_de=101, exploitant=None, date_debut=date(2024, 1, 1),
        )
        data = BeneficierDeSerializer(bd).data
        self.assertIsNone(data['properties']['exploitant_nom'])

    def test_abri_description_is_none_when_no_abri_urgence(self):
        bd = BeneficierDe.objects.create(
            id_beneficier_de=102, abri_urgence=None, date_debut=date(2024, 1, 1),
        )
        data = BeneficierDeSerializer(bd).data
        self.assertIsNone(data['properties']['abri_description'])


# ============================================================================
# PlanDeSuiviSerializer
# ============================================================================

class PlanDeSuiviSerializerTest(TestCase):
    """Tests for the type_suivi_detail and unite_pastorale_detail nested fields."""

    def test_type_suivi_detail_contains_description(self):
        ts = TypeDeSuivi.objects.create(id_type_suivi=100, description='SuiviDesc')
        up = UnitePastorale.objects.create(
            id_unite_pastorale=103, code_up='UP103', nom_up='UP103 Nom',
            annee_version=2024, geometry=_up_geom(), version_active=True,
        )
        plan = PlanDeSuivi.objects.create(
            id_plan_suivi=100, description='Plan100',
            type_suivi=ts, unite_pastorale=up,
        )
        data = PlanDeSuiviSerializer(plan).data
        self.assertIn('description', data['type_suivi_detail'])

    def test_unite_pastorale_detail_contains_nom_up(self):
        ts = TypeDeSuivi.objects.create(id_type_suivi=101, description='SuiviDesc2')
        up = UnitePastorale.objects.create(
            id_unite_pastorale=104, code_up='UP104', nom_up='UP104 Nom',
            annee_version=2024, geometry=_up_geom(), version_active=True,
        )
        plan = PlanDeSuivi.objects.create(
            id_plan_suivi=101, description='Plan101',
            type_suivi=ts, unite_pastorale=up,
        )
        data = PlanDeSuiviSerializer(plan).data
        self.assertIn('nom_up', data['unite_pastorale_detail'])


# ============================================================================
# MesureDePlanSerializer
# ============================================================================

class MesureDePlanSerializerTest(TestCase):
    """Tests for the type_mesure_detail and plan_suivi_detail nested fields."""

    def _make_plan(self):
        return PlanDeSuivi.objects.create(id_plan_suivi=102, description='PlanBase')

    def test_type_mesure_detail_contains_description(self):
        tm = TypeDeMesure.objects.create(id_type_mesure=100, description='MesureDesc')
        plan = self._make_plan()
        mesure = MesureDePlan.objects.create(
            id_mesure_plan=100, description='Mesure100',
            type_mesure=tm, plan_suivi=plan,
        )
        data = MesureDePlanSerializer(mesure).data
        self.assertIn('description', data['type_mesure_detail'])

    def test_plan_suivi_detail_contains_description(self):
        plan = self._make_plan()
        mesure = MesureDePlan.objects.create(
            id_mesure_plan=101, description='Mesure101', plan_suivi=plan,
        )
        data = MesureDePlanSerializer(mesure).data
        self.assertIn('description', data['plan_suivi_detail'])


# ============================================================================
# SubventionPNVSerializer
# ============================================================================

class SubventionPNVSerializerTest(TestCase):
    """Tests for the exploitant_detail nested field."""

    def test_exploitant_detail_contains_nom_exploitant(self):
        exp = Exploitant.objects.create(id_exploitant=104, nom_exploitant='ExpSub')
        sub = SubventionPNV.objects.create(
            id_subvention=100, description='Sub100',
            montant=Decimal('1000.00'), exploitant=exp,
        )
        data = SubventionPNVSerializer(sub).data
        self.assertIn('nom_exploitant', data['exploitant_detail'])


# ============================================================================
# LogementCommoditeSerializer
# ============================================================================

class LogementCommoditeSerializerTest(TestCase):
    """Tests for the logement_code and commodite_desc source-based fields."""

    def test_logement_code_and_commodite_desc_match_source_values(self):
        log = Logement.objects.create(logement_code='L100')
        com = Commodite.objects.create(id_commodite=100, description='Eau chaude')
        lc = LogementCommodite.objects.create(
            id_logement_commodite=100, logement=log, commodite=com, etat='Bon',
        )
        data = LogementCommoditeSerializer(lc).data
        self.assertEqual(data['logement_code'], 'L100')
        self.assertEqual(data['commodite_desc'], 'Eau chaude')


# ============================================================================
# Simple field-presence tests (one method per serializer)
# ============================================================================

class TypeConventionSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        tc = TypeConvention.objects.create(id_type_convention=100, description='Conv100')
        data = TypeConventionSerializer(tc).data
        self.assertIn('id_type_convention', data)
        self.assertIn('description', data)


class TypeDeSuiviSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        ts = TypeDeSuivi.objects.create(id_type_suivi=103, description='Suivi103')
        data = TypeDeSuiviSerializer(ts).data
        self.assertIn('id_type_suivi', data)
        self.assertIn('description', data)


class TypeDeMesureSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        tm = TypeDeMesure.objects.create(id_type_mesure=101, description='Mesure101')
        data = TypeDeMesureSerializer(tm).data
        self.assertIn('id_type_mesure', data)
        self.assertIn('description', data)


class BergerSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        b = Berger.objects.create(
            id_berger=101, nom_berger='Renard', prenom_berger='Paul',
        )
        data = BergerSerializer(b).data
        self.assertIn('nom_berger', data)
        self.assertIn('prenom_berger', data)


class TypeCheptelSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        tc = TypeCheptel.objects.create(
            id_type_cheptel=101, description='Ovin', espece='Ovins',
        )
        data = TypeCheptelSerializer(tc).data
        self.assertIn('id_type_cheptel', data)
        self.assertIn('description', data)
        self.assertIn('espece', data)


class ProductionSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        p = Production.objects.create(id_production=100, description='Lait')
        data = ProductionSerializer(p).data
        self.assertIn('id_production', data)
        self.assertIn('description', data)


class Categorie_pensionSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        cp = Categorie_pension.objects.create(
            id_categorie_pension=100, description='PensionTest',
        )
        data = Categorie_pensionSerializer(cp).data
        self.assertIn('id_categorie_pension', data)
        self.assertIn('description', data)


class EspeceSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        e = Espece.objects.create(id_espece=100, description='Caprin')
        data = EspeceSerializer(e).data
        self.assertIn('id_espece', data)
        self.assertIn('description', data)


class RaceSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        esp = Espece.objects.create(id_espece=101, description='Bovin')
        r = Race.objects.create(id_race=100, description='Salers', espece=esp)
        data = RaceSerializer(r).data
        self.assertIn('id_race', data)
        self.assertIn('description', data)
        self.assertIn('espece', data)


class Categorie_animauxSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        esp = Espece.objects.create(id_espece=102, description='Ovin')
        ca = Categorie_animaux.objects.create(
            id_categorie_animaux=100, description='Agneau', espece=esp,
        )
        data = Categorie_animauxSerializer(ca).data
        self.assertIn('id_categorie_animaux', data)
        self.assertIn('description', data)
        self.assertIn('espece', data)


class CheptelSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        elev = Eleveur.objects.create(id_eleveur=110, nom_eleveur='ElevCheptel')
        sit = SituationDExploitation.objects.create(
            id_situation=105, nom_situation='SitCheptel', situation_active=True,
        )
        cheptel = Cheptel.objects.create(
            id_cheptel=100, description='Troupeau100',
            eleveur=elev, situation_exploitation=sit, nombre_animaux=50,
        )
        data = CheptelSerializer(cheptel).data
        self.assertIn('id_cheptel', data)
        self.assertIn('description', data)


class Type_cheptelSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        tc = Type_cheptel.objects.create(
            id_type_cheptel=100, description='TypeCheptelTest',
        )
        data = Type_cheptelSerializer(tc).data
        self.assertIn('id_type_cheptel', data)
        self.assertIn('description', data)


class TypeEvenementSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        te = TypeEvenement.objects.create(
            id_type_evenement=100, description='Incendie',
        )
        data = TypeEvenementSerializer(te).data
        self.assertIn('id_type_evenement', data)
        self.assertIn('description', data)


class TypeEquipementSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        te = TypeEquipement.objects.create(
            id_type_equipement=100, description='Clôture', categorie='Alpage',
        )
        data = TypeEquipementSerializer(te).data
        self.assertIn('id_type_equipement', data)
        self.assertIn('description', data)
        self.assertIn('categorie', data)


class AbriDUrgenceSerializerFieldsTest(TestCase):
    def test_fields_present(self):
        a = AbriDUrgence.objects.create(
            id_abri_urgence=100, description='Cabane100', etat='Bon',
        )
        data = AbriDUrgenceSerializer(a).data
        self.assertIn('id_abri_urgence', data)
        self.assertIn('description', data)
        self.assertIn('etat', data)
