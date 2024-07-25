from django.contrib import admin

# Register your models here.
from .models import Stok
from .models import Siparis
from .models import Kargo
from .models import Blog
from .forms import SiparisFormu


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')

class SiparisAdmin(admin.ModelAdmin):
    form = SiparisFormu
    list_display = ('id', 'Firmaadi', 'Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Toplam', 'Komisyon', 'Komisyontutari')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'Baslik', 'Metin', 'Url')

class KargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Siparisno', 'Desi', 'Kargotutari', 'Hizmetbedeli', 'Toplam')

admin.site.register(Stok,StokAdmin)
admin.site.register(Siparis,SiparisAdmin)
admin.site.register(Kargo,KargoAdmin)
admin.site.register(Blog,BlogAdmin)