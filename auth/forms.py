from django import forms
from user.models import User
from django.contrib.auth.models import User as DjangoUser


class UserAuthForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DjangoUserAuthForm(forms.ModelForm):

    class Meta:
        model = DjangoUser
        fields = ('username', 'password')
