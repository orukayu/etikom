from django.conf import settings
from django.db import models
import datetime

class Kargo(models.Model):
    Siparisno = models.CharField(max_length=25, null=True)
    Desi = models.IntegerField()
    Kargotutari = models.DecimalField(max_digits=10, decimal_places=2)
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['Siparisno']  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Siparisno)

class Siparis(models.Model):
    Siparisno = models.CharField(max_length=25)
    Pazaryeri = models.CharField(max_length=25)
    Tarih = models.DateField()
    Stokkodu = models.CharField(max_length=25)
    Adet = models.PositiveIntegerField()
    Satisfiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    Komisyon = models.DecimalField(max_digits=10, decimal_places=2)
    Komisyontutari = models.DecimalField(max_digits=10, decimal_places=2)
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save3(self, *args, **kwargs):
        self.Toplam = self.Adet * self.Satisfiyati
        self.Komisyontutari = self.Toplam * self.Komisyon / 100
        super().save(*args, **kwargs)

    def save4(self, *args, **kwargs):       # şimdilik kullanılmıyor. Formda ikinci butona basıldığında yapılacak işlem için örnek duruyor.
        self.Adet = self.Adet * -1
        self.Toplam = self.Adet * self.Satisfiyati
        self.Kalan = self.Toplam - self.Komisyon - self.Kargo - self.Hibedeli - self.Isbedeli
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Siparisno

class Stok(models.Model):
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Afaturano = models.CharField(max_length=20)
    Stokkodu = models.CharField(max_length=20)
    Adet = models.IntegerField()
    Alisfiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save1(self, *args, **kwargs):
        self.Toplam = self.Adet * self.Alisfiyati
        super().save(*args, **kwargs)

    def save2(self, *args, **kwargs):   # Şimdilik kullanılmıyor. Modele ikinci butona basıldığında yapılacak kaydetme için örnek duruyor.
        self.Adet = self.Adet * -1
        self.Toplam = self.Adet * self.Alisfiyati
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Stokkodu

class Blog(models.Model):
    Baslik = models.TextField()
    Metin = models.TextField()
    Url = models.SlugField(unique=True)

    class Meta:
        ordering = ['Baslik',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Baslik