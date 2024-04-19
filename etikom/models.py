from django.conf import settings
from django.db import models
from django.utils import timezone

class Stok(models.Model):
    Afaturano = models.CharField(max_length=20)
    Stokkodu = models.CharField(max_length=20)
    Adet = models.IntegerField()
    Alisfiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplam = models.DecimalField(max_digits=10, decimal_places=2)
    
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