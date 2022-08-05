from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from web.auth_app.serializers import error_messages

User = get_user_model()


@tag('auth')
class AuthApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'rahmatovolim3@gmail.com',
            'password': make_password("tester26")
        }
        cls.user = User.objects.create(**data)

    def test_login(self):
        login_url = reverse_lazy("auth_app:sign-in")
        data = {
            "email": self.user.email,
            "password": "tester26"
        }
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        data['password'] = 'wrong_password'
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json().get("email"), [error_messages['wrong_credentials']])
        """ Logout """
        url = reverse_lazy('auth_app:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_up(self):
        url = reverse_lazy('auth_app:sign-up')
        data = {
            "first_name": "Olim",
            "last_name": "Rakhmatov",
            "email": "new_user@gmail.com",
            "password1": "tester20",
            "password2": "tester21",
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json().get("non_field_errors"), [error_messages['password_not_match']], response.data)
        data['password2'] = 'tester20'
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {"email": [error_messages['already_registered']]}, response.data)





