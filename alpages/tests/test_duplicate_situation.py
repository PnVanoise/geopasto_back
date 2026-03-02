from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date

from alpages.models import SituationDExploitation, Exploiter, Ruche, GardeSituation, Elever, QuartierPasto, Berger, Eleveur, TypeCheptel

class DuplicateSituationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # create and authenticate a test user because the API requires authentication
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        # create a situation
        self.orig = SituationDExploitation.objects.create(
            id_situation=1,
            nom_situation='Origine',
            situation_active=True,
            date_debut=date(2020,1,1),
            date_fin=None,
        )
        # create related objects
        # Create required related FK objects
        quartier = QuartierPasto.objects.create(id_quartier=1, code_quartier='Q1', nom_quartier='Q1')
        berger = Berger.objects.create(id_berger=1, nom_berger='B', prenom_berger='B')
        eleveur = Eleveur.objects.create(id_eleveur=1, nom_eleveur='E')
        type_cheptel = TypeCheptel.objects.create(id_type_cheptel=1, description='T')

        Exploiter.objects.create(id_exploiter=1, quartier=quartier, situation_exploitation=self.orig, date_debut=date(2020,1,1), commentaire='c')
        Ruche.objects.create(id_ruche=1, description='R1', geometry='POINT(0 0)', situation_exploitation=self.orig)
        GardeSituation.objects.create(id_garde_situation=1, date_debut=date(2020,1,1), commentaire='g', situation_exploitation=self.orig, berger=berger)
        Elever.objects.create(id_elever=1, situation_exploitation=self.orig, type_cheptel=type_cheptel, eleveur=eleveur, nombre_animaux=5, pension='P', date_debut=date(2020,1,1))

    def test_duplicate_clones_and_closes_original(self):
        url = reverse('situationexploitation-duplicate', kwargs={'pk': self.orig.id_situation})
        # call duplicate
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        # new situation should be active and have date_debut today
        new_id = data.get('id_situation')
        self.assertIsNotNone(new_id)
        new = SituationDExploitation.objects.get(id_situation=new_id)
        self.assertTrue(new.situation_active)
        self.assertEqual(new.date_debut, date.today())
        # original should be inactive and date_fin today
        orig = SituationDExploitation.objects.get(id_situation=self.orig.id_situation)
        self.assertFalse(orig.situation_active)
        self.assertEqual(orig.date_fin, date.today())
        # related counts: new should have clones
        self.assertEqual(new.exploitations.count(), 1)
        self.assertEqual(new.ruches.count(), 1)
        self.assertEqual(new.gardes_situation.count(), 1)
        from alpages.models import Elever
        self.assertEqual(Elever.objects.filter(situation_exploitation=new).count(), 1)
        # check linked relationships point to new
        ex = new.exploitations.first()
        self.assertEqual(ex.situation_exploitation.id_situation, new.id_situation)
        ru = new.ruches.first()
        self.assertEqual(ru.situation_exploitation.id_situation, new.id_situation)
        gr = new.gardes_situation.first()
        self.assertEqual(gr.situation_exploitation.id_situation, new.id_situation)
        el = Elever.objects.filter(situation_exploitation=new).first()
        self.assertEqual(el.situation_exploitation.id_situation, new.id_situation)
