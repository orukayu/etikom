from django import forms

from .models import Stok

class PostForm(forms.ModelForm):

    class Meta:
        model = Stok
        fields = ('Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')
        labels = {"Stokkodu" : "Stok Kodu", "Alisfiyati" : "Alış Fiyatı", "Afaturano" : "Fatura Numarası"}