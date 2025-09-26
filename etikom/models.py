from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal # Decimal tipi için import ekle

class Faturakontrol(models.Model):
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Pazaryeri = models.CharField(max_length=50, null=True, blank=True)
    Siparisno = models.CharField(max_length=50)
    Tarih = models.DateField(null=True, blank=True)
    Stokkodu = models.CharField(max_length=50)
    Siparisadet = models.IntegerField(null=True, blank=True)
    Iadeadet = models.IntegerField(null=True, blank=True)
    Adet = models.IntegerField(null=True, blank=True)
    Satisfiyati = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Toplamsatistutari = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Pazaryeriindirimi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Komisyonorani = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Komisyontutari = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Alisfiyati = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Alistoplami = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Kargodesi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Kargotutari = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Hizmetbedeli = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Islembedeli = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Iadedesi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Iadetutari = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Kalan = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save7(self, *args, **kwargs):
        # Hesaplama öncesi tüm alanların None olup olmadığını kontrol et ve 0'a çevir
        self.Iadeadet = self.Iadeadet if self.Iadeadet is not None else Decimal(0)
        self.Adet = self.Siparisadet - self.Iadeadet
        self.Toplamsatistutari = self.Adet * self.Satisfiyati
        self.Pazaryeriindirimi = self.Pazaryeriindirimi if self.Pazaryeriindirimi is not None else Decimal(0)
        self.Komisyontutari = self.Komisyontutari if self.Komisyontutari is not None else Decimal(0)
        self.Kargodesi = self.Kargodesi if self.Kargodesi is not None else Decimal(0)
        self.Kargotutari = self.Kargotutari if self.Kargotutari is not None else Decimal(0)
        self.Iadedesi = self.Iadedesi if self.Iadedesi is not None else Decimal(0)
        self.Iadetutari = self.Iadetutari if self.Iadetutari is not None else Decimal(0)
        self.Alistoplami = self.Alistoplami if self.Alistoplami is not None else Decimal(0)
        self.Hizmetbedeli = self.Hizmetbedeli if self.Hizmetbedeli is not None else Decimal(0)
        self.Islembedeli = self.Islembedeli if self.Islembedeli is not None else Decimal(0)

        # Yeni hesaplama mantığı
        self.Komisyontutari = self.Toplamsatistutari * self.Komisyonorani / 100
        
        # Kalan değerinin hesaplanması
        self.Kalan = self.Toplamsatistutari + self.Pazaryeriindirimi - self.Komisyontutari - self.Kargotutari - self.Iadetutari - self.Alistoplami - self.Hizmetbedeli - self.Islembedeli
        
        super().save(*args, **kwargs)

    def save8(self, *args, **kwargs):
        # Hesaplama öncesi tüm alanların None olup olmadığını kontrol et ve 0'a çevir
        self.Kargodesi = self.Kargodesi if self.Kargodesi is not None else Decimal(0)
        self.Kargotutari = self.Kargotutari if self.Kargotutari is not None else Decimal(0)
        self.Hizmetbedeli = self.Hizmetbedeli if self.Hizmetbedeli is not None else Decimal(0)
        self.Islembedeli = self.Islembedeli if self.Islembedeli is not None else Decimal(0)

        # Kalan değerinin hesaplanması
        self.Kalan = self.Toplamsatistutari + self.Pazaryeriindirimi - self.Komisyontutari - self.Kargotutari - self.Iadetutari - self.Alistoplami - self.Hizmetbedeli - self.Islembedeli
        
        super().save(*args, **kwargs)

    def save9(self, *args, **kwargs):
        # Hesaplama öncesi tüm alanların None olup olmadığını kontrol et ve 0'a çevir
        self.Iadeadet = self.Iadeadet if self.Iadeadet is not None else Decimal(0)
        self.Adet = self.Siparisadet - self.Iadeadet
        self.Toplamsatistutari = self.Adet * self.Satisfiyati
        self.Alistoplami = self.Adet * self.Alisfiyati
        self.Komisyontutari = self.Toplamsatistutari * self.Komisyonorani / 100
        self.Iadedesi = self.Iadedesi if self.Iadedesi is not None else Decimal(0)
        self.Iadetutari = self.Iadetutari if self.Iadetutari is not None else Decimal(0)

        # Kalan değerinin hesaplanması
        self.Kalan = self.Toplamsatistutari + self.Pazaryeriindirimi - self.Komisyontutari - self.Kargotutari - self.Iadetutari - self.Alistoplami - self.Hizmetbedeli - self.Islembedeli
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return f"{self.Siparisno} - {self.Stokkodu}"

class Iade(models.Model):
    Siparisno = models.CharField(max_length=25)
    Stokkodu = models.CharField(max_length=25)
    Adet = models.PositiveIntegerField()
    Desi = models.IntegerField()
    Iadetutari = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Tur = models.CharField(max_length=20)

    def save6(self, *args, **kwargs):
        self.Toplam = self.Iadetutari * 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Siparisno)


class Kargo(models.Model):
    Siparisno = models.CharField(max_length=25, null=True)
    Stokkodu = models.CharField(max_length=25, null=True)
    Desi = models.IntegerField()
    Kargotutari = models.DecimalField(max_digits=10, decimal_places=2)
    Hizmetbedeli = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Islembedeli = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Tur = models.CharField(max_length=20, null=True)

    def save5(self, *args, **kwargs):
        self.Toplam = self.Kargotutari + self.Hizmetbedeli + self.Islembedeli
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Siparisno)

class Siparis(models.Model):
    Siparisno = models.CharField(max_length=25)
    Pazaryeri = models.CharField(max_length=25)
    Tarih = models.DateField(null=True, blank=True)
    Stokkodu = models.CharField(max_length=25)
    Adet = models.IntegerField()
    Satisfiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    Komisyon = models.DecimalField(max_digits=10, decimal_places=2)
    Komisyontutari = models.DecimalField(max_digits=10, decimal_places=2)
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Tur = models.CharField(max_length=20, null=True)
    
    def save3(self, *args, **kwargs):
        self.Toplam = self.Adet * self.Satisfiyati
        self.Komisyontutari = self.Toplam * self.Komisyon / 100
        super().save(*args, **kwargs)

    def save4(self, *args, **kwargs):
        self.Toplam = self.Adet * self.Satisfiyati
        self.Komisyontutari = self.Toplam * self.Komisyon / 100
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
    Tur = models.CharField(max_length=20, null=True)
    Alistarihi = models.DateField(null=True, blank=True)
    
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

class Gider(models.Model):
    Firmaadi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Baslik = models.TextField()
    Tarih = models.DateField(null=True, blank=True)
    Tutar = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-Tarih',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Baslik