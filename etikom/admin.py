from django.contrib import admin

# Register your models here.
from .models import Stok
from .models import Siparis
from .models import Kargo
from .models import Iade
from .models import Blog
from .models import Gider
from .forms import SiparisFormu


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Tur', 'Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')

class SiparisAdmin(admin.ModelAdmin):
    form = SiparisFormu
    list_display = ('id', 'Firmaadi', 'Tur', 'Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Toplam', 'Komisyon', 'Komisyontutari')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'Baslik', 'Metin', 'Url')

class KargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Tur', 'Siparisno', 'Stokkodu', 'Desi', 'Kargotutari', 'Hizmetbedeli', 'Toplam')

class IadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Tur', 'Siparisno', 'Desi', 'Iadetutari', 'Stokkodu', 'Adet', 'Toplam')

class GiderAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Baslik', 'Tarih', 'Tutar')

admin.site.register(Stok,StokAdmin)
admin.site.register(Siparis,SiparisAdmin)
admin.site.register(Kargo,KargoAdmin)
admin.site.register(Iade,IadeAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Gider,GiderAdmin)