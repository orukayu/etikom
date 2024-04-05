from django.contrib import admin

# Register your models here.
from .models import Stok


class StokAdmin(admin.ModelAdmin):
    list_display = ('id', 'Stokkodu', 'Adet', 'Alisfiyati', 'Toplam', 'Afaturano')


admin.site.register(Stok,StokAdmin)