from unittest import mock

from django.test import TestCase
from django.test.client import RequestFactory

from firebase_auth.authentication import FirebaseAuthentication
from firebase_auth.tests.helpers import (
    create_user, mock_firebase_uid, mock_token, mock_verify_id_token,
)


class FirebaseAuthenticationTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_authenticate_with_no_token_fails(self):
        request = self.request_factory.get('/')
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    def test_authenticate_with_empty_token_fails(self):
        request = self.request_factory.get('/', HTTP_AUTHORIZATION='')
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    @mock.patch(
        'firebase_admin.auth.verify_id_token',
        side_effect=mock_verify_id_token)
    def test_authenticate_with_valid_token_and_no_user_fails(self, mock_instance):
        request = self.request_factory.get('/', HTTP_AUTHORIZATION=mock_token)
        user = FirebaseAuthentication().authenticate(request)
        assert user is None

    @mock.patch(
        'firebase_admin.auth.verify_id_token',
        side_effect=mock_verify_id_token)
    def test_authenticate_with_valid_token_and_user_passes(self, mock_instance):
        request = self.request_factory.get('/', HTTP_AUTHORIZATION=mock_token)
        expected_user = create_user(firebase_uid=mock_firebase_uid)
        authenticated_user = FirebaseAuthentication().authenticate(request)
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
