from django import forms
from django.contrib.auth.models import User
from .models import Account

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ийм и-мэйлтэй хэрэглэгч аль хэдийн бүртгэгдсэн.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Нууц үгүүд тохирохгүй байна.")
        return cleaned

class AccountForm(forms.ModelForm):
    phone_number = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Утас'}))
    pro_image = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['phone_number', 'pro_image']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'readonly':'readonly'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    pro_image = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['phone_number', 'pro_image']
