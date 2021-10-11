from django import forms

from contacts.models import Contact


class SingInForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']
