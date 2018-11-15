from firebase_auth.models import User


mock_token = 'valid_token'
mock_firebase_uid = mock_token

def mock_verify_id_token(token, app):
    return {
        'uid': token,
    }

def create_user(firebase_uid=mock_token, email='email@gmail.com'):
    user = User.objects.create(email=email, firebase_uid=firebase_uid)
    user.set_password('supersekret')
    user.save()
    return user
