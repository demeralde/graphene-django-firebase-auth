from django.contrib.auth import get_user_model
from firebase_admin import auth

from firebase_auth.apps import firebase_app
from firebase_auth.forms import UserRegistrationForm


User = get_user_model()


class FirebaseAuthentication:

    def _get_auth_token(self, request):
        encoded_token = request.META.get('HTTP_AUTHORIZATION')
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(encoded_token, firebase_app, True)
        except ValueError:
            pass
        except auth.AuthError:
            pass
        return decoded_token

    def _register_unregistered_user(self, firebase_uid):
        user = None
        form = UserRegistrationForm(data={
            'firebase_uid': firebase_uid,
        })

        if form.is_valid():
            user = form.save()
        errors = form.errors
        return user

    def _get_user_from_token(self, decoded_token):
        firebase_uid = decoded_token.get('uid')
        user = None

        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            user = self._register_unregistered_user(firebase_uid)
        return user

    def authenticate(self, request):
        user = None
        decoded_token = self._get_auth_token(request)

        if decoded_token:
            user = self._get_user_from_token(decoded_token)
        return user

    def get_user(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user = None
        return user
