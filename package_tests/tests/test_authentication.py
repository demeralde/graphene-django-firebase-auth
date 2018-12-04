# pylint: disable=W0212
from django.test import TestCase
from django.test.client import RequestFactory

from firebase_auth.authentication import FirebaseAuthentication
from package_tests.tests.helpers import (
    create_user, setup_mocks, stub_firebase_uid, stub_firebase_token,
)
from package_tests.models import User


setup_mocks()


class FirebaseAuthenticationTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_auth_token_with_no_token_returns_none(self):
        request = self.request_factory.get('/')
        token = FirebaseAuthentication()._get_auth_token(request)
        assert token is None

    def test_get_auth_token_with_empty_token_returns_none(self):
        request = self.request_factory.get(
            '/',
            HTTP_AUTHORIZATION='',
        )
        token = FirebaseAuthentication()._get_auth_token(request)
        assert token is None

    def test_get_auth_token_with_invalid_token_returns_none(self):
        request = self.request_factory.get(
            '/',
            HTTP_AUTHORIZATION='invalid',
        )
        token = FirebaseAuthentication()._get_auth_token(request)
        assert token is None

    def test_get_auth_token_with_valid_token_returns_user(self):
        request = self.request_factory.get(
            '/',
            HTTP_AUTHORIZATION=stub_firebase_token,
        )
        token = FirebaseAuthentication()._get_auth_token(request)
        assert token == {
            'uid': stub_firebase_uid,
        }

    def test_register_unregistered_user_with_empty_uid_returns_none(self):
        received_user = FirebaseAuthentication()._register_unregistered_user('')
        assert User.objects.count() == 0
        assert received_user is None

    def test_register_unregistered_user_with_invalid_uid_returns_none(self):
        received_user = FirebaseAuthentication()._register_unregistered_user('invalid_uid')
        assert User.objects.count() == 0
        assert received_user is None

    def test_register_unregistered_user_with_valid_uid_returns_user(self):
        assert User.objects.count() == 0

        uid = stub_firebase_uid
        received_user = FirebaseAuthentication()._register_unregistered_user(uid)
        assert User.objects.count() == 1

        expected_user = User.objects.get(firebase_uid=uid)
        assert received_user == expected_user

    def test_get_user_from_token_with_empty_token_returns_none(self):
        token = {
            'uid': '',
        }
        received_user = FirebaseAuthentication()._get_user_from_token(token)
        assert User.objects.count() == 0
        assert received_user is None

    def test_get_user_from_token_with_invalid_token_returns_none(self):
        token = {
            'uid': 'invalid',
        }
        received_user = FirebaseAuthentication()._get_user_from_token(token)
        assert User.objects.count() == 0
        assert received_user is None

    def test_get_user_from_token_with_valid_token_returns_user(self):
        token = {
            'uid': stub_firebase_uid,
        }
        assert User.objects.count() == 0
        received_user = FirebaseAuthentication()._get_user_from_token(token)
        expected_user = User.objects.get(firebase_uid=token['uid'])
        assert User.objects.count() == 1
        assert received_user == expected_user

    def test_authenticate_with_no_token_returns_none(self):
        request = self.request_factory.get('/')
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    def test_authenticate_with_empty_token_returns_none(self):
        request = self.request_factory.get('/', HTTP_AUTHORIZATION='')
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    def test_authenticate_with_invalid_token_returns_none(self):
        request = self.request_factory.get('/', HTTP_AUTHORIZATION='invalid')
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    def test_authenticate_with_valid_token_and_no_user_returns_user(self):
        request = self.request_factory.get(
            '/',
            HTTP_AUTHORIZATION=stub_firebase_token,
        )
        assert User.objects.count() == 0
        received_user = FirebaseAuthentication().authenticate(request)
        assert User.objects.count() == 1
        expected_user = User.objects.get(firebase_uid=stub_firebase_uid)
        assert received_user == expected_user

    def test_authenticate_with_valid_token_and_user_returns_user(self):
        request = self.request_factory.get(
            '/',
            HTTP_AUTHORIZATION=stub_firebase_token,
        )
        expected_user = create_user(firebase_uid=stub_firebase_uid)
        assert User.objects.count() == 1
        authenticated_user = FirebaseAuthentication().authenticate(request)
        assert User.objects.count() == 1
        assert authenticated_user == expected_user

    def test_get_user_with_no_user_returns_none(self):
        user = FirebaseAuthentication().get_user(user_pk=None)
        assert user is None

    def test_get_user_with_valid_pk_returns_user(self):
        expected_user = create_user()
        user = FirebaseAuthentication().get_user(user_pk=expected_user.pk)
        assert user.pk == expected_user.pk

    def test_get_user_with_invalid_pk_returns_none(self):
        user = FirebaseAuthentication().get_user(user_pk=3)
        assert user is None
