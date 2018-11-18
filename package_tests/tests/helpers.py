from firebase_admin import auth

from package_tests.models import User


mock_firebase_token = 'mock_firebase_token'
mock_firebase_uid = 'mock_firebase_uid'

def mock_firebase_verify_id_token(token, app):
    return {
        'uid': mock_firebase_uid,
    }

def mock_firebase_get_user(firebase_uid):
    if firebase_uid == mock_firebase_uid:
        return {
            'uid': mock_firebase_uid,
        }
    raise auth.AuthError(code='USER_NOT_FOUND', message='User not found.')

def create_user(firebase_uid=mock_firebase_uid, email='email@gmail.com'):
    user = User.objects.create(email=email, firebase_uid=firebase_uid)
    user.set_password('supersekret')
    user.save()
    return user
