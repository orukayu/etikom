from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.girisyap, name='girisurl'),
    path('hakkimizda/', views.hakkimizdayap, name='hakkimizdaurl'),
    path('fiyatlandirma/', views.fiyatlamayap, name='fiyatlamaurl'),
    path('iletisim/', views.iletisimyap, name='iletisimurl'),
    path('blog/', views.blogyap, name='blogurl'),
    path('raporlar/', views.raporlaryap, name='raporlarurl'),

    path('fiyat-hesapla/', views.fiyathesaplamayap, name='fiyathesaplaurl'),

    path('stok-ekle/', views.stokeklemeyap, name='stokekleurl'),
    path('stok-listesi/', views.stoklistesiyap, name='stoklistesiurl'),
    path('stok-exceli-yukle/', views.stokexceliyuklemeyap, name='stokexceliyukleurl'),
    path('stok-hareketleri/', views.stokharaketleriyap, name='stokhareketleriurl'),
    path('stok-hareketleri/<str:sort>/', views.stokharaketleriyap, name='hareketsiralamaurl'),

    path('siparis-ekle/', views.sipariseklemeyap, name='siparisekleurl'),
    path('siparis-listesi/', views.siparislistesiyap, name='siparislistesiurl'),
    path('siparis-listesi/<str:sort>/', views.siparislistesiyap, name='siparissiralama'),
    path('siparis-exceli-yukle/', views.sipexceliyuklemeyap, name='sipexceliyukleurl'),
    path('siparis-icerikleri/<int:sira>', views.siparisleritoplayap, name='siparisleritoplaurl'),

    path('kargo-ekle/', views.kargoeklemeyap, name='kargoekleurl'),
    path('kargo-exceli-yukle/', views.kargoexceliyuklemeyap, name='kargoexceliyukleurl'),
    path('kargo-listesi/', views.kargolistesiyap, name='kargolistesiurl'),
    path('kargo-listesi/<str:sort>/', views.kargolistesiyap, name='kargosiralamaurl'),

    path('iade-ekle/', views.iadeeklemeyap, name='iadeekleurl'),
    path('iade-exceli-yukle/', views.iadeexceliyuklemeyap, name='iadeexceliyukleurl'),
    path('iade-listesi/', views.iadelistesiyap, name='iadelistesiurl'),
    path('iade-listesi/<str:sort>/', views.iadelistesiyap, name='iadesiralamaurl'),

    path('gider-ekle/', views.gidereklemeyap, name='giderekleurl'),
    path('gider-exceli-yukle/', views.giderexceliyuklemeyap, name='giderexceliyukleurl'),
    path('gider-listesi/', views.giderlistesiyap, name='giderlistesiurl'),
    path('gider-listesi/<str:sort>/', views.giderlistesiyap, name='gidersiralamaurl'),







    path('stok-duzeltme/<str:firma>/<int:pk>/', views.stokduzeltme, name='stokduzeltmeurl'),
    
    path('stok-exceli-indir/', views.stokexceliindir, name='stokexcelindirurl'),
    path('sayim-exceli-indir/', views.sayimexcelindir, name='sayimexcelindirurl'),

    path('fatura-detayi/<str:sort>/', views.stokfaturasi, name='stokfaturasiurl'),
    path('stok-detayi/<str:sort>/', views.stokgecmisi, name='stokgecmisiurl'),



    
    

    
    path('siparis-topla-exceli/<int:sira>', views.siparistoplaexceli, name='siptoplaexcelindirurl'),

    path('siparis-yok/', views.siparisyok, name='siparisyokurl'),

    
    

    path('siparis-duzeltme/<str:firma>/<int:pk>/', views.siparisduzeltme, name='siparisduzeltmeurl'),
    path('siparis-exceli-indir/', views.sipexceliindir, name='sipexcelindirurl'),

    path('pazaryeri-detayi/<str:pzr>/', views.pazaryeridetay, name='pazaryeridetayurl'),
    path('siparis-detayi/<str:sort>/', views.siparisdetay, name='siparisdetayurl'),



    
    

    

    path('kargo-duzeltme/<str:firma>/<int:pk>/', views.kargoduzeltme, name='kargoduzeltmeurl'),
    path('kargo-exceli-indir/', views.kargoexceliindir, name='kargoexcelindirurl'),



    
    

    
    
    path('iade-duzeltme/<str:firma>/<int:pk>/', views.iadeduzeltme, name='iadeduzeltmeurl'),
    path('iade-exceli-indir/', views.iadeexceliindir, name='iadeexcelindirurl'),


    
    

    

    path('gider-duzeltme/<str:firma>/<int:pk>/', views.giderduzeltme, name='giderduzeltmeurl'),
    path('gider-exceli-indir/', views.giderexceliindir, name='giderexcelindirurl'),

    path('baslik-detayi/<str:sort>/', views.baslikdetayi, name='baslikdetayiurl'),

    
    
    path('blog/<str:url>/', views.blogdetayyap, name='blogdetayurl'),
    
    path('kayit-ol/', views.kayitol, name='kayitolurl'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),

    path("robots.txt", TemplateView.as_view(template_name="etikom/robots.txt", content_type="text/plain")),
]