from django.urls import path
from . import views


urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('anasayfa/', views.demofirma, name='demofirmaurl'),
    path('stok-listesi/', views.stokliste, name='stoklistesiurl'),
    path('stok-listesi/<str:sort>/', views.stokliste, name='stoksiralama'),
    path('siparis-listesi/', views.siparisliste, name='siparislistesi'),
    path('siparis-listesi/<str:sort>/', views.siparisliste, name='siparissiralama'),
    path('kayit-ol/', views.kayitol, name='kayit-ol'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),
    path('giris/', views.girisyap, name='girisurl'),
    path('iletisim/', views.iletisimyap, name='iletisimurl'),
    path('hakkimizda/', views.hakkimizdayap, name='hakkimizdaurl'),
    path('fiyatlandirma/', views.fiyatlamayap, name='fiyatlamaurl'),
    path('stok-exceli-yukle/', views.stokexcelyuklemeyap, name='stokexcelyukleurl'),
    path('siparis-exceli-yukle/', views.sipexcelyuklemeyap, name='sipexcelyukleurl'),
]