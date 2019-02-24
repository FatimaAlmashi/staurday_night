from django import forms
from .models import Movie
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['added_by']

        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password',]

        widgets = {
            'password': forms.PasswordInput(),
        }


class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if " " in username or "@" in username:
            raise forms.ValidationError("Incorrect username format")
        return username
