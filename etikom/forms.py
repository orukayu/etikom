from django import forms
from .models import Stok
from .models import Siparis

class GirisFormu(forms.Form):
    firma_adi = forms.CharField(label='Firma Adı')
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)

class KayitFormu(forms.Form):     
    firma_adi = forms.CharField(label='Firma Adı')
    email = forms.EmailField(label='E-posta Adresi')    
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifreyi Tekrar Girin', widget=forms.PasswordInput)


class SiparisFormu(forms.ModelForm):

    class Meta:
        model = Siparis
        fields = ('Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Komisyon')
        labels = {"Komisyon" : "Komisyon (%)", "Siparisno" : "Sipariş No", "Tarih" : "Sipariş Tarihi", "Stokkodu" : "Stok Kodu", "Satisfiyati" : "Satış Fiyatı"}
        widgets = {            
            'Pazaryeri': forms.TextInput(attrs={'placeholder': 'Trendyol, HB, N11 vb.'}),
            'Tarih': forms.TextInput(attrs={'placeholder': '2024-04-28'}),
            'Siparisno': forms.TextInput(attrs={'placeholder': '2155139405'}),
            'Stokkodu': forms.TextInput(attrs={'placeholder': 'AB1030'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4'}),
            'Satisfiyati': forms.TextInput(attrs={'placeholder': '137.50'}),
            'Komisyon': forms.TextInput(attrs={'placeholder': '9.60'}),
        }

class StokFormu(forms.ModelForm):

    class Meta:
        model = Stok
        fields = ('Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')
        labels = {"Stokkodu" : "Stok Kodu", "Alisfiyati" : "Fiyat", "Afaturano" : "Fatura No"}
        widgets = {
            'Afaturano': forms.TextInput(attrs={'placeholder': 'FTR202400001234'}),
            'Stokkodu': forms.TextInput(attrs={'placeholder': 'iPhone 12'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4'}),
            'Alisfiyati': forms.TextInput(attrs={'placeholder': '27.50'}),
            'Toplam': forms.TextInput(attrs={'placeholder': '110'}),
        }

