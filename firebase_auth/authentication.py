import firebase_admin
from django.conf import settings
from django.contrib.auth import get_user_model
from firebase_admin import auth


User = get_user_model()

credentials = firebase_admin.credentials.Certificate(settings.FIREBASE_KEY_FILE)
app = firebase_admin.initialize_app(credentials)


class FirebaseAuthentication:

    def authenticate(self, request):
        encoded_token = request.META.get('HTTP_AUTHORIZATION')

        try:
            decoded_token = auth.verify_id_token(encoded_token, app)
        except Exception:
            return None

        token_uid = decoded_token.get('uid')
        try:
            user = User.objects.get(firebase_uid=token_uid)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user = None
        return user
