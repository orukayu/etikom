from django import forms

from .models import Stok

class StokForm(forms.ModelForm):

    class Meta:
        model = Stok
        fields = ('Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')
        labels = {"Stokkodu" : "Stok Kodu", "Alisfiyati" : "Fiyat", "Afaturano" : "Fatura No"}
        widgets = {
            'Afaturano': forms.TextInput(attrs={'placeholder': 'FTR2024000375'}),
            'Stokkodu': forms.TextInput(attrs={'placeholder': 'AB1030'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4'}),
            'Alisfiyati': forms.TextInput(attrs={'placeholder': '7.50'}),
            'Toplam': forms.TextInput(attrs={'placeholder': '30'}),
        }