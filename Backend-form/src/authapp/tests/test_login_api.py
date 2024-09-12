import unittest
import requests

class APILoginTestCase(unittest.TestCase):
    base_url = 'http://127.0.0.1:8000/auth/login/'

    def test_login_success(self):
        data = {'email': 'inpathtamilan@onedatasoftware.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['message'], 'Login successful')

    def test_login_invalid_username(self):
        data = {'username': 'ram', 'password': 'ram123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json()['message'], 'Invalid username or password')

    def test_login_invalid_password(self):
        data = {'username': 'inpathtamilan@onedatasoftware.com', 'password': 'invalid_password'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json()['message'], 'Invalid username or password')

    def test_login_empty_username(self):
        data = {'username': '', 'password': 'valid_password'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Username is required')

    def test_login_empty_password(self):
        data = {'username': 'valid_username', 'password': ''}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Password is required')

    def test_login_whitespace_username(self):
        data = {'username': ' ', 'password': 'valid_password'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Username is required')

    def test_login_whitespace_password(self):
        data = {'username': 'valid_username', 'password': '   '}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Password is required')

    def test_login_invalid_credentials(self):
        data = {'username': 'invalid_username', 'password': 'invalid_password'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json()['message'], 'Invalid username or password')

    def test_login_case_insensitive_password(self):
        data = {'username': 'valid_username', 'password': 'VaLiD_PaSsWoRd'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json()['message'], 'Invalid username or password')

if __name__ == '__main__':
    unittest.main(verbosity=2)




