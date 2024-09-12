import unittest
import requests

class APISignupTestCase(unittest.TestCase):
    base_url = 'http://127.0.0.1:8000/auth/signup/'

    def test_signup_success(self):
        data = {'username': 'Tamilan', 'email': 'tamilan@gmail.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json()['message'], 'Signup successful')

    def test_signup_admin_success(self):
        data = {'username': 'nataraj', 'email': 'nataraj@gmail.com', 
                'password': 'Tamilan123*',
                "token":"aa3dd9b7-17f8-4860-8941-d2d5d935177a"}

        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)

    def test_signup_existing_username(self):
        data = {'username': 'tamilan', 'email': 'test@gmail.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Username already exists')

    def test_signup_existing_email(self):
        data = {'username': 'new_user', 'email': 'inpathtamilan@onedatasoftware.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Email already exists')

    def test_signup_empty_username(self):
        data = {'username': '', 'email': 'new_user@example.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Username is required')

    def test_signup_empty_email(self):
        data = {'username': 'new_user', 'email': '', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Email is required')

    def test_signup_empty_password(self):
        data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': ''}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Password is required')

    def test_signup_weak_password(self):
        data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'password'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Password must contain at least one uppercase letter, one lowercase letter, and one digit')

    def test_signup_invalid_email(self):
        data = {'username': 'new_user', 'email': 'invalid_email', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Invalid email format')

    def test_signup_username_case_insensitive(self):
        data = {'username': 'TaMiLan', 'email': 'test@example.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json()['message'], 'Signup successful')

    def test_signup_email_case_insensitive(self):
        data = {'username': 'new_user', 'email': 'nEw_UsEr@exAmPle.com', 'password': 'Tamilan123*'}
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json()['message'], 'Signup successful')

if __name__ == '__main__':
    unittest.main(verbosity=2)
