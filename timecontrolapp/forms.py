from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import UserCreationForm

from .models import Company


class SignUpForm(UserCreationForm):
    company = forms.ModelChoiceField(label='Компания', queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.CharField(label='Должность', max_length=50)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'company', 'position']