
from django import forms
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from .models import Blog

class UserRegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(
                                    attrs=dict(required=True, max_length=30)),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=30)))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=dict(required=True, max_length=30, render_value=False)))

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            _("The username already exists. Please try another one."))


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ('username', 'password')


class BlogAdditionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=40)))
    blog_text = forms.CharField(
        widget=forms.Textarea(attrs=dict(required=True)))


class CommentAdditionForm(forms.Form):
    comment_text = forms.CharField(label="Add Comment",
                                   widget=forms.Textarea(
                                       attrs=dict(required=True, rows=3)))


class BlogUpdateForm(forms.ModelForm):
    '''
    title = forms.CharField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=40)))
    blog_text = forms.CharField(
        widget=forms.Textarea(attrs=dict(required=True)))'''
    class Meta:
        model = Blog
        fields = ['title', 'blog_text']
