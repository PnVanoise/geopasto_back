import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_token_and_userpermissions():
    username = 'testuser'
    password = 'testpass'
    # create user
    user = User.objects.create_user(username=username, password=password)

    client = APIClient()

    # obtain JWT token
    resp = client.post('/api/token/', {'username': username, 'password': password}, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data
    access = resp.data['access']

    # call userpermissions endpoint
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    resp2 = client.get('/api/userpermissions/')
    assert resp2.status_code == 200
    data = resp2.data
    assert data.get('username') == username
    assert isinstance(data.get('permissions_by_model'), dict)
