from django import forms

class CarpmaFormu(forms.Form):
    sayi1 = forms.IntegerField(label='1. Sayı')
    sayi2 = forms.IntegerField(label='2. Sayı')


from django.forms import ModelForm
from .models import Sayilar

class SayilarFormu(ModelForm):
    class Meta:
        model = Sayilar
        fields = ['sayi1', 'sayi2', 'sayi3']
