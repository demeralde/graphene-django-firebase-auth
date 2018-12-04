from firebase_admin import auth

from package_tests.models import User


# Stubs

stub_firebase_token = 'stub_firebase_token'
stub_firebase_uid = 'stub_firebase_uid'

stub_email = 'daniel@danieljs.tech'
stub_username = 'dspacejs'


# Mock classes

class MockUserRecord(object):
    email = None
    display_name = None
    uid = None

    def __init__(self, email, display_name, uid):
        self.email = email
        self.display_name = display_name
        self.uid = uid


# Mock methods

def mock_firebase_verify_id_token(encoded_token, app, check_revoked):
    if encoded_token == stub_firebase_token:
        return {
            'uid': stub_firebase_uid,
        }
    elif encoded_token is None:
        raise ValueError('Token is not valid.')
    elif encoded_token == '':
        raise ValueError('Token is not valid.')
    raise auth.AuthError(code='USER_NOT_FOUND', message='User not found.')

def mock_firebase_get_user(firebase_uid):
    if firebase_uid == stub_firebase_uid:
        return MockUserRecord(
            email=stub_email,
            display_name=stub_username,
            uid=stub_firebase_uid,
        )
    raise auth.AuthError(code='USER_NOT_FOUND', message='User not found.')

def create_user(firebase_uid=stub_firebase_uid, email='email@gmail.com'):
    user = User.objects.create(email=email, firebase_uid=firebase_uid)
    user.set_password('supersekret')
    user.save()
    return user

def setup_mocks():
    auth.verify_id_token = mock_firebase_verify_id_token
    auth.get_user = mock_firebase_get_user
