from django.contrib import admin

# Register your models here.
from .models import Stok
from .models import Siparis


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')


class SiparisAdmin(admin.ModelAdmin):
    list_display = ('id', 'Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Toplam', 'Komisyon', 'Komisyontutari', 'Firmaadi')


admin.site.register(Stok,StokAdmin)
admin.site.register(Siparis,SiparisAdmin)