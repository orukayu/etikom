from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

class KullaniciKayitFormu(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', max_length=32)
    email = forms.EmailField(label='E-posta Adresi')
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifreyi Tekrar Girin', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Şifreler eşleşmiyor.')
        return password2

class Stok(models.Model):
    Stokkodu = models.CharField(max_length=20)
    Adet = models.IntegerField()
    Alisfiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    Afaturano = models.CharField(max_length=20)

    def save1(self, *args, **kwargs):
        self.Toplam = self.Adet * self.Alisfiyati
        super().save(*args, **kwargs)

    def save2(self, *args, **kwargs):
        self.Adet = self.Adet * -1
        self.Toplam = self.Adet * self.Alisfiyati
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['Stokkodu',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Stokkodu