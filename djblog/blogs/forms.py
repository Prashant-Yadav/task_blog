
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'confirm_password', 'first_name', 'last_name')

    def clean(self):
        if ('password1' in self.cleaned_data) and ('password2' in self.cleaned_data):
            if (self.cleaned_data['password1']) != (self.cleaned_data['password2']):
                raise forms.ValidationError(
                    "The two password fields did not match.")
        return self.cleaned_data


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ('username', 'password')
