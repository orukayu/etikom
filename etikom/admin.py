from django.contrib import admin

# Register your models here.
from .models import Stok
from .models import Siparis


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam', 'Afaturano')


class SiparisAdmin(admin.ModelAdmin):
    list_display = ('id', 'Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Toplam', 'Komisyon', 'Kargo', 'Hibedeli', 'Isbedeli', 'Kalan')


admin.site.register(Stok,StokAdmin)
admin.site.register(Siparis,SiparisAdmin)