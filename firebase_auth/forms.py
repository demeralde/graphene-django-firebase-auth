from django import forms
from django.contrib.auth import get_user_model
from firebase_admin import auth


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['firebase_uid', User.USERNAME_FIELD] \
            + list(User.REQUIRED_FIELDS)

    def clean_firebase_uid(self):
        firebase_uid = self.data['firebase_uid']

        try:
            # Ensure the specified user exists in Firebase
            user = auth.get_user(firebase_uid)
            self.data['email'] = user.email
            self.data['username'] = user.display_name
        except auth.AuthError:
            raise forms.ValidationError('The firebase_uid is invalid.')
        except ValueError:
            raise forms.ValidationError('The firebase_uid is invalid.')

        return firebase_uid
