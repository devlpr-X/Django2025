from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Account
from django.core.exceptions import ValidationError

class RegisterForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Энэ цахим шуудан аль хэдийн бүртгэлтэй байна.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('repeat_password')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Нууц үг таарахгүй байна.")
        return cleaned

    def save(self, commit=True):
        user = super(ModelForm, self).save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.username = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AccountForm(ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone', 'class': 'form-control'}), required=False)
    pro_image = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ('phone_number', 'pro_image')
