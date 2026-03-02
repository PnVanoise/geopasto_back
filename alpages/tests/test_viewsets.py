from datetime import date
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth import get_user_model

from alpages.models import SituationDExploitation, Commodite, AbriDUrgence


class ViewsetsSmokeTest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='vtest', password='vtest')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # create a minimal UnitePastorale required by SituationDExploitation serializer
        from alpages.models import UnitePastorale
        UnitePastorale.objects.create(id_unite_pastorale=1, code_up='UP1', nom_up='UP1', annee_version=2025, geometry='MULTIPOLYGON(((0 0,0 1,1 1,1 0,0 0)))', version_active=True)

    def test_create_and_list_commodite(self):
        url = reverse('commodite-list')
        resp = self.client.post(url, {'id_commodite': 30, 'description': 'C30'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        list_resp = self.client.get(url)
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_resp.json()), 1)

    def test_create_situation_and_list(self):
        url = reverse('situationexploitation-list')
        # send date as ISO string for JSON payload
        payload = {'id_situation': 30, 'nom_situation': 'S30', 'situation_active': True, 'date_debut': date.today().isoformat(), 'unite_pastorale': 1}
        resp = self.client.post(url, payload, format='json')
        # If creation fails, include response data in assertion message for easier debugging
        if resp.status_code != status.HTTP_201_CREATED:
            print('DEBUG create situation response:', resp.status_code, resp.content)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_abri_endpoint_create(self):
        url = reverse('abridurgence-list')
        resp = self.client.post(url, {'id_abri_urgence': 30, 'description': 'A30', 'etat': 'OK'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
