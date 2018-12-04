from django.test import TestCase

from firebase_auth.forms import UserRegistrationForm
from package_tests.tests.helpers import (
    stub_email, stub_firebase_uid, setup_mocks, stub_username,
)


setup_mocks()


class UserRegistrationFormTests(TestCase):

    def test_fields(self):
        assert UserRegistrationForm.Meta.fields == [
            'firebase_uid', 'username', 'email',
        ]

    def test_valid_data(self):
        firebase_uid = stub_firebase_uid
        form = UserRegistrationForm(data={
            'firebase_uid': firebase_uid,
        })
        assert form.is_valid()

        saved_user = form.save()
        assert saved_user.firebase_uid == firebase_uid
        assert saved_user.email == stub_email
        assert saved_user.username == stub_username

    def test_invalid_firebase_uid(self):
        form = UserRegistrationForm(data={
            'firebase_uid': 'invalid_firebase_uid',
        })
        assert not form.is_valid()
