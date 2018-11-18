from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from firebase_auth.models import FirebaseAuthMixin


class User(AbstractBaseUser, PermissionsMixin, FirebaseAuthMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
