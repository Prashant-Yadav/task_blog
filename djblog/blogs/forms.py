
from django import forms
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from .models import Blog


class UserRegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(
                                    attrs={'required': True, 'max_length': 30, 'class': 'form-control'}),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'required': True, 'max_length': 30, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': True, 'max_length': 30, 'render_value': False, 'class': 'form-control'}))

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            _("The username already exists. Please try another one."))


class AuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('username', 'password')


class BlogAdditionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'required': True, 'max_length': 40, 'class': 'form-control'}))
    blog_text = forms.CharField(widget=forms.Textarea(
        attrs={'required': True, 'class': 'form-control'}))


class CommentAdditionForm(forms.Form):
    comment_text = forms.CharField(label="Add Comment",
                                   widget=forms.Textarea(
                                       attrs={'required': True, 'rows': 3, 'class': 'form-control'}))


class BlogUpdateForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'blog_text']
