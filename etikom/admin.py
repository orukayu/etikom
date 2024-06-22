from django.contrib import admin

# Register your models here.
from .models import Stok
from .models import Siparis
from .models import Blog
from .forms import SiparisFormu


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Firmaadi', 'Afaturano', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam')


class SiparisAdmin(admin.ModelAdmin):
    form = SiparisFormu
    list_display = ('id', 'Pazaryeri', 'Tarih', 'Siparisno', 'Stokkodu', 'Adet', 'Satisfiyati', 'Toplam', 'Komisyon', 'Komisyontutari', 'Firmaadi')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'Baslik', 'Metin', 'Url')

admin.site.register(Stok,StokAdmin)
admin.site.register(Siparis,SiparisAdmin)
admin.site.register(Blog,BlogAdmin)