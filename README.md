# graphene-django-firebase-auth

Authentication provider for graphene-django and Firebase's Authentication service.

Note this is a WIP and abandoned project since I never ended up using Firebase. But the code is still a good starting point as of writing this.

Partially inspired by
[django-firebase-auth](https://github.com/fcornelius/django-firebase-auth)
for Django REST framework.

This app is used with [Firebase Authentication](https://firebase.google.com/docs/auth/) on a client.

## Compatibility

This code has only been tested with Python `3.7.0` and Django `2.1.2`.

## Installing

1. Install the app:

```sh
pipenv install graphene-django-firebase-auth
```

2. Download the JSON file from your [Firebase console](https://console.firebase.google.com/) with your account's credentials.

3. Set `FIREBASE_KEY_FILE` in your project's settings to the path of the credentials file:

```python
FIREBASE_KEY_FILE = os.path.join(BASE_DIR, 'path/to/firebase-credentials.json')
```

4. Add the authentication backend to `AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = ['firebase_auth.authentication.FirebaseAuthentication']
```

5. Add `firebase_auth` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
  '...',
  'firebase_auth',
]
```

6. Add `FirebaseAuthMixin` to your `AUTH_USER_MODEL`:

```python
class User(PermissionsMixin, FirebaseAuthMixin):
    # ...
```

7. Build and run your DB migrations to add the changes:

```sh
./manage.py makemigrations
./manage.py migrate
```

## Using the package

Once installed, authentication will be managed using this package.
You can access `info.context.user` to add authentication logic, such as
with the following:

```python
def resolve_users(self, info, **kwargs):
    success = False

    if info.context.user.is_authenticated:
        success = True
    return success
```

## Sending tokens on the client

Your client will need to send an `Authorization: Bearer` token on each request. How you do this depends on your client and is outside the scope
of this documentation.

## Developing

### Setting up your environment

1. Install the dependencies:

```sh
pipenv install -d
```

2. Download the JSON file from your [Firebase console](https://console.firebase.google.com/) with your account's credentials.

3. Create an `.env` file using `.env.example` as a template. Make sure
to specify the path to the file in the previous step.

4. Enter the virtual environment:

```sh
./manage.py shell
```

### Other commands

```sh
# Run the tests
./manage.py test
```

```sh
# Lint the code
./lint.sh
```
