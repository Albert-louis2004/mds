from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import *
import time
import os
import json
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ["name", "manufacturer", "memory", "ssd", "processor", "image", "price", "quantity"]
        labels = {
            "name": "Nume",
            "manufacturer": "Producător",
            "memory": "Memorie",
            "ssd": "SSD",
            "processor": "Procesor",
            "image": "Imagine",
            "price": "Preț",
            "quantity": "Cantitate",
        }
def validate_name(value):
    if not value.istitle() or not value.isalpha():
        messages.warning("Numele si prenumele gresite")
        logger.warning("Nume si prenume gresite")
        raise ValidationError('Numele și prenumele trebuie să înceapă cu literă mare și să conțină doar litere și spații.')

def validate_subject(value):
    if not value.istitle():
        messages.warning("Subiectul nu incepe cu litera mare")
        logger.warning("Subiectul trebuie sa inceapa cu litera mare")
        raise ValidationError('Subiectul trebuie să înceapă cu literă mare.')

def validate_message(value):
    words = value.split()
    if len(words) < 5 or len(words) > 100:
        messages.warning('Mesajul contine prea putine sau prea multe cuvinte')
        raise ValidationError('Mesajul trebuie să conțină între 5 și 100 de cuvinte.')
    if 'http://' in value or 'https://' in value:
        messages.warning("Mesajul nu trebuie sa contina linkuri")
        logger.error("Mesajul nu are voie sa contina linkuri")
        raise ValidationError('Mesajul nu trebuie să conțină link-uri.')
    if value.startswith('http://') or value.startswith('https://'):
        messages.error('Mesajul nu trebuie sa inceapa cu un link')
        logger.error("Mesajul nu are voie sa inceapa cu un link")
        raise ValidationError('Mesajul nu trebuie să înceapă cu "http://" sau "https://".')

def validate_age(value):
    today = date.today()
    age_years = today.year - value.year
    age_months = today.month - value.month
    if today.day < value.day:
        age_months -= 1
    if age_months < 0:
        age_years -= 1
        age_months += 12
    if age_years < 18:
        messages.info('Varsta minima este de 18 ani')
        raise ValidationError('Trebuie să aveți cel puțin 18 ani.')

class ContactForm(forms.Form):
    NAME_CHOICES = [
        ('reclamatie', 'Reclamație'),
        ('intrebare', 'Întrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare')
    ]
    
    nume = forms.CharField(label='Nume', max_length=100, validators=[validate_name])
    prenume = forms.CharField(label='Prenume', max_length=100, validators=[validate_name])
    data_nasterii = forms.DateField(label='Data Nașterii', widget=forms.TextInput(attrs={'type': 'date'}), validators=[validate_age])
    email = forms.EmailField(label='Email')
    confirmare_email = forms.EmailField(label='Confirmare Email')
    tip_mesaj = forms.ChoiceField(label='Tip Mesaj', choices=NAME_CHOICES)
    subiect = forms.CharField(label='Subiect', max_length=200, validators=[validate_subject])
    minim_zile_asteptare = forms.IntegerField(label='Minim Zile Așteptare')
    mesaj = forms.CharField(label='Mesaj', widget=forms.Textarea, validators=[validate_message])

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirmare_email = cleaned_data.get("confirmare_email")
        data_nasterii = cleaned_data.get("data_nasterii")

        if email != confirmare_email:
            raise forms.ValidationError("Emailul și Confirmarea Emailului nu se potrivesc.")

        if data_nasterii:
            # Calcularea vârstei în ani și luni
            today = date.today()
            age_years = today.year - data_nasterii.year
            age_months = today.month - data_nasterii.month
            if today.day < data_nasterii.day:
                age_months -= 1
            if age_months < 0:
                age_years -= 1
                age_months += 12

            cleaned_data['varsta'] = f"{age_years} ani și {age_months} luni"

        # Elimină confirmarea emailului și data nașterii din datele salvate
        cleaned_data.pop('confirmare_email')
        if 'data_nasterii' in cleaned_data:
            cleaned_data.pop('data_nasterii')

        # Salvarea datelor în fișier JSON
        timestamp = int(time.time())
        filename = f'mesaj_{timestamp}.json'
        filepath = os.path.join('mesaje', filename)

        # Creează directorul dacă nu există
        if not os.path.exists('mesaje'):
            os.makedirs('mesaje')

        # Salvează datele în fișier JSON
        with open(filepath, 'w') as json_file:
            json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)
            print(f"Fișier salvat: {filepath}")

        return cleaned_data
    

class UserRegistrationForm(UserCreationForm): 
    email = forms.EmailField(label='Email',required=True)
    
class Meta: 
    model = User 
    fields = ('username', 'email', 'password1','password2')

def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        password_confirm = cleaned_data.get('password2')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Parolele nu sunt identice')
        return cleaned_data