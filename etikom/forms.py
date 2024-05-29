from django import forms
from .models import Stok
from .models import Siparis
from django.utils.dateparse import parse_date


class GirisFormu(forms.Form):
    firma_adi = forms.CharField(label='Firma Adı')
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)

class KayitFormu(forms.Form):     
    firma_adi = forms.CharField(label='Firma Adı')
    email = forms.EmailField(label='E-posta Adresi')    
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifreyi Tekrar Girin', widget=forms.PasswordInput)


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
            'Pazaryeri': forms.TextInput(attrs={'placeholder': 'Trendyol, HB, N11 vb.'}),
            'Tarih': forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': '28/04/2024'}),
            'Siparisno': forms.TextInput(attrs={'placeholder': '2155139405'}),
            'Adet': forms.TextInput(attrs={'placeholder': '4'}),
            'Satisfiyati': forms.TextInput(attrs={'placeholder': '137.50'}),
            'Komisyon': forms.TextInput(attrs={'placeholder': '9.60'}),
        }

        input_formats = {
            'Tarih': ['%d-%m-%Y'],
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['Stokkodu'].queryset = Stok.objects.filter(Firmaadi=user).values_list('Stokkodu', flat=True).order_by('Stokkodu').distinct()


    def clean_Tarih(self):
        tarih = self.cleaned_data['Tarih']
        if not tarih:
            raise forms.ValidationError("Lütfen tarihi 'gg/aa/yyyy' formatında girin.")
        return tarih

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

