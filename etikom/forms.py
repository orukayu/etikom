from django import forms
from .models import Stok
from .models import Siparis
from .models import Kargo
from .models import Iade
from .models import Gider
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

class GiderFormu(forms.ModelForm):
    class Meta:
        model = Gider
        fields = ['Baslik', 'Tarih', 'Tutar']
        labels = {"Baslik" : "Başlık", "Tarih" : "Tarih", "Tutar" : "Tutar"}
        widgets = {
            'Baslik': forms.TextInput(attrs={'placeholder': 'Kira Gideri', 'class': 'form-control', 'id': 'baslik'}),
            'Tutar': forms.TextInput(attrs={'placeholder': '12500.00', 'class': 'form-control', 'id': 'tutar'}),
        }
    Tarih = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'tarih'}),
    )

class IadeFormu(forms.ModelForm):
    class Meta:
        model = Iade
        fields = ['Siparisno', 'Stokkodu', 'Adet', 'Desi', 'Iadetutari']
        labels = {"Siparisno" : "Sipariş No", "Stokkodu" : "Stok Kodu", "Adet" : "Adet", "Desi" : "Desi", "Iadetutari" : "İade Kargo Tutarı"}
        widgets = {
            'Siparisno': forms.TextInput(attrs={'placeholder': 'Sipariş listesinden ...', 'class': 'form-control', 'id': 'siparisno'}),
            'Stokkodu': forms.TextInput(attrs={'placeholder': 'Sipariş içeriğinden ...', 'class': 'form-control', 'id': 'stokkodu'}),
            'Adet': forms.TextInput(attrs={'placeholder': '1', 'class': 'form-control', 'id': 'adet'}),
            'Desi': forms.TextInput(attrs={'placeholder': '3', 'class': 'form-control', 'id': 'desi'}),
            'Iadetutari': forms.TextInput(attrs={'placeholder': '27.50', 'class': 'form-control', 'id': 'iadetutari'}),
        }


class KargoFormu(forms.ModelForm):
    class Meta:
        model = Kargo
        fields = ['Siparisno', 'Desi', 'Kargotutari', 'Hizmetbedeli']
        labels = {"Siparisno" : "Sipariş No", "Desi" : "Desi", "Kargotutari" : "Kargo Tutarı", "Hizmetbedeli" : "Hizmet+İşlem Bedeli"}
        widgets = {
            'Siparisno': forms.TextInput(attrs={'placeholder': 'Sipariş listesinden ...', 'class': 'form-control', 'id': 'siparisno'}),
            'Desi': forms.TextInput(attrs={'placeholder': '3', 'class': 'form-control', 'id': 'desi'}),
            'Kargotutari': forms.TextInput(attrs={'placeholder': '27.50', 'class': 'form-control', 'id': 'kargotutari'}),
            'Hizmetbedeli': forms.TextInput(attrs={'placeholder': '5.99', 'class': 'form-control', 'id': 'hizmetbedeli'}),
        }


class GirisFormu(forms.Form):
    firma_adi = forms.CharField(label='Firma Adı')
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)

class KayitFormu(forms.Form):
    firma_adi = forms.CharField(
        label='Firma Adı',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'firmaadi'})
    )
    email = forms.EmailField(
        label='E-posta Adresi',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    password1 = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})
    )
    password2 = forms.CharField(
        label='Şifreyi Tekrar Girin',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'})
    )

    def clean_firma_adi(self):
        firma_adi = self.cleaned_data.get('firma_adi')

        # Sadece harf, rakam ve alt çizgiye izin ver
        if not re.match(r'^[a-zA-Z0-9_ğüşçöıĞÜŞÇÖİ ]+$', firma_adi):
            raise ValidationError("Firma adı yalnızca harf, rakam ve boşluk içerebilir. Özel karakterler ve HTML etiketleri yasaktır.")

        return firma_adi

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Şifreler eşleşmiyor.")


class SiparisFormu(forms.ModelForm):

    Stokkodu = forms.ModelChoiceField(
        queryset=Stok.objects.none(),
        to_field_name="Stokkodu",
        widget=forms.Select,
        label="Stok Kodu"
    )

    class Meta:
        model = Siparis
        fields = ('Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Komisyon')
        labels = {"Komisyon" : "Komisyon (%)", "Siparisno" : "Sipariş No", "Tarih" : "Sipariş Tarihi", "Stokkodu" : "Stok Kodu", "Satisfiyati" : "Satış Fiyatı"}
        widgets = {            
            'Pazaryeri': forms.TextInput(attrs={'placeholder': 'Trendyol, HB, N11 vb.', 'class': 'form-control', 'id': 'pazaryeri'}),
            'Siparisno': forms.TextInput(attrs={'placeholder': '2155139405', 'class': 'form-control', 'id': 'siparisno'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4', 'class': 'form-control', 'id': 'adet'}),
            'Satisfiyati': forms.TextInput(attrs={'placeholder': '137.50', 'class': 'form-control', 'id': 'satisfiyati'}),
            'Komisyon': forms.TextInput(attrs={'placeholder': '9.60', 'class': 'form-control', 'id': 'komisyon'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['Stokkodu'].queryset = Stok.objects.filter(Firmaadi=user.id).values_list('Stokkodu', flat=True).order_by('Stokkodu').distinct()
        if self.instance and self.instance.pk:
            self.fields['Stokkodu'].initial = self.instance.Stokkodu

    Tarih = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'tarih'}),
    )

class StokFormu(forms.ModelForm):

    class Meta:
        model = Stok
        fields = ('Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')
        labels = {"Stokkodu" : "Stok Kodu", "Alisfiyati" : "Alış Fiyatı", "Afaturano" : "Fatura No"}
        widgets = {
            'Afaturano': forms.TextInput(attrs={'placeholder': 'FTR202400001234', 'class': 'form-control', 'id': 'faturano'}),
            'Stokkodu': forms.TextInput(attrs={'placeholder': 'iPhone 12', 'class': 'form-control', 'id': 'stokkodu'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4', 'class': 'form-control', 'id': 'adet'}),
            'Alisfiyati': forms.TextInput(attrs={'placeholder': '27.50', 'class': 'form-control', 'id': 'alisfiyati'}),
            'Toplam': forms.TextInput(attrs={'placeholder': '110.00', 'class': 'form-control', 'id': 'toplam'}),
        }

