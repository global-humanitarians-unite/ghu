from django import forms
from django.core.exceptions import ValidationError
from ghu_global.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
# from ghu_main.models import Profile

def unused_username(username):
    if User.objects.filter(username=username).count() > 0:
        raise ValidationError('Username {} is already in use.'.format(username))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=User._meta.get_field('username').max_length,
                               validators=(UnicodeUsernameValidator, unused_username))
    password = forms.CharField(widget=forms.PasswordInput, validators=(validate_password,))

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'])
        # # Make a profile for this user
        # profile = Profile.objects.create(user=user)
        # # For now, make everyone who registers a User
        # # XXX Don't hardcode this
        # profile.set_group('Users')
        # profile.save()

        return user

class SearchForm(forms.Form):
    search_terms = forms.CharField(label = 'Search', max_length = 100, required = False)
