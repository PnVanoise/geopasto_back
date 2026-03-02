from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class PermissionsSmokeTest(APITestCase):

    def test_unauthenticated_cannot_list_commodite(self):
        url = reverse('commodite-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
