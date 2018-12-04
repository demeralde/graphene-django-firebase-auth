from django.apps import AppConfig
from django.conf import settings
import firebase_admin


firebase_app = None


class FirebaseAuthConfig(AppConfig):
    name = 'firebase_auth'

    def ready(self):
        credentials = firebase_admin.credentials.Certificate(
            settings.GOOGLE_APPLICATION_CREDENTIALS,
        )
        global firebase_app
        firebase_app = firebase_admin.initialize_app(credentials)
