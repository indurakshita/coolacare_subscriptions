import pytest
import requests
from django.urls import reverse

def test_api_login():
    url = reverse('login')  # Assuming your login URL is named 'login' in your URLconf
    data = {'email': 'inpathtamilan@onedatasoftware.com', 'password': 'Tamilan123*'}
    response = requests.post(f'http://127.0.0.1:8000{url}', json=data)
    
    assert response.status_code == 200
    assert 'token' in response.json()
    
