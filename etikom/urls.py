from django.urls import path
from . import views


urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('anasayfa/', views.demofirma, name='demofirmaurl'),

    path('stok-ekle/', views.stokeklemeyap, name='stokekleurl'),
    path('stok-exceli-yukle/', views.stokexcelyuklemeyap, name='stokexcelyukleurl'),

    path('stok-listesi/', views.sayimliste, name='stoklistesiurl'),
    path('stok-listesi/<str:sort>/', views.sayimliste, name='stoksiralamaurl'),

    path('stok-hareketleri/', views.stokliste, name='stokhareketleriurl'),
    path('stok-hareketleri/<str:sort>/', views.stokliste, name='hareketsiralamaurl'),

    path('stok-duzeltme/<str:firma>/<int:pk>/', views.stokduzeltme, name='stokduzeltmeurl'),
    
    path('stok-exceli-indir/', views.stokexceliindir, name='stokexcelindirurl'),
    path('sayim-exceli-indir/', views.sayimexcelindir, name='sayimexcelindirurl'),

    path('islem-detayi/<str:sort>/', views.stokfaturasi, name='stokfaturasiurl'),
    path('stok-gecmisi/<str:sort>/', views.stokgecmisi, name='stokgecmisiurl'),

    path('siparis-ekle/', views.siparisekleme, name='siparisekleurl'),
    path('siparis-exceli-yukle/', views.sipexcelyuklemeyap, name='sipexcelyukleurl'),

    path('siparis-listesi/', views.siparisliste, name='siparislistesiurl'),
    path('siparis-listesi/<str:sort>/', views.siparisliste, name='siparissiralama'),

    path('siparis-duzeltme/<str:firma>/<int:pk>/', views.siparisduzeltme, name='siparisduzeltmeurl'),
    path('siparis-exceli-indir/', views.sipexceliindir, name='sipexcelindirurl'),

    path('pazaryeri-detayi/<str:pzr>/', views.pazaryeridetay, name='pazaryeridetayurl'),



    path('giris/', views.girisyap, name='girisurl'),
    path('hakkimizda/', views.hakkimizdayap, name='hakkimizdaurl'),
    path('fiyatlandirma/', views.fiyatlamayap, name='fiyatlamaurl'),
    path('iletisim/', views.iletisimyap, name='iletisimurl'),
    
    path('kayit-ol/', views.kayitol, name='kayitolurl'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),
]