from unittest import mock

from django.test import TestCase

from firebase_auth.forms import UserRegistrationForm
from .helpers import mock_firebase_get_user, mock_firebase_uid


class UserRegistrationFormTests(TestCase):

    def test_fields(self):
        assert UserRegistrationForm.Meta.fields == [
            'firebase_uid', 'username', 'email',
        ]

    @mock.patch(
        'firebase_admin.auth.get_user',
        side_effect=mock_firebase_get_user,
    )
    def test_valid_data(self, mock_instance):
        firebase_uid = mock_firebase_uid
        username = 'dspacejs'
        email = 'daniel@danieljs.tech'

        form = UserRegistrationForm(data={
            'firebase_uid': firebase_uid,
            'username': username,
            'email': email,
        })
        assert form.is_valid()

        saved_user = form.save()
        assert saved_user.firebase_uid == firebase_uid
        assert saved_user.email == email
        assert saved_user.username == username

    @mock.patch(
        'firebase_admin.auth.get_user',
        side_effect=mock_firebase_get_user,
    )
    def test_invalid_firebase_uid(self, mock_instance):
        form = UserRegistrationForm(data={
            'firebase_uid': 'invalid_firebase_uid',
            'username': 'dspacejs',
            'email': 'daniel@danieljs.tech',
        })
        assert not form.is_valid()
