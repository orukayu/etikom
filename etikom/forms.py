from django import forms

from .models import Stok

class GirisFormu(forms.Form):     
    firma_adi = forms.CharField(label='Firma Adı')
    email = forms.EmailField(label='E-posta Adresi')    
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifreyi Tekrar Girin', widget=forms.PasswordInput)

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