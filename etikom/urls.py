from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.girisyap, name='girisurl'),
    path('hakkimizda/', views.hakkimizdayap, name='hakkimizdaurl'),
    path('fiyatlandirma/', views.fiyatlamayap, name='fiyatlamaurl'),
    path('iletisim/', views.iletisimyap, name='iletisimurl'),
    path('blog/', views.blogyap, name='blogurl'),
    path('blog/<str:url>/', views.blogdetayyap, name='blogdetayurl'),
    path('genel-raporlar/', views.raporlaryap, name='raporlarurl'),
    path('fatura-kontrol/', views.kontrolyap, name='faturakontrolurl'),

    path('fiyat-hesapla/', views.fiyathesaplamayap, name='fiyathesaplaurl'),

    path('stok-ekle/', views.stokeklemeyap, name='stokekleurl'),
    path('stok-listesi/', views.stoklistesiyap, name='stoklistesiurl'),
    path('stok-gecmisi/<str:sort>/', views.stokgecmisiyap, name='stokgecmisiurl'),
    path('stok-exceli-yukle/', views.stokexceliyuklemeyap, name='stokexceliyukleurl'),
    path('stok-hareketleri/', views.stokharaketleriyap, name='stokhareketleriurl'),
    path('stok-hareketleri/<str:sort>/', views.stokharaketleriyap, name='hareketsiralamaurl'),
    path('stok-haraket-detayi/<str:firma>/<int:pk>/', views.stokharaketdetayiyap, name='stokharaketdetayiurl'),

    path('siparis-ekle/', views.sipariseklemeyap, name='siparisekleurl'),
    path('siparis-listesi/', views.siparislistesiyap, name='siparislistesiurl'),
    path('siparis-listesi/<str:sort>/', views.siparislistesiyap, name='siparissiralama'),
    path('siparis-detayi/<str:sort>/', views.siparisdetayiyap, name='siparisdetayurl'),
    path('siparis-exceli-yukle/', views.sipexceliyuklemeyap, name='sipexceliyukleurl'),
    path('siparis-icerikleri/<int:sira>', views.siparisleritoplayap, name='siparisleritoplaurl'),
    path('siparis-duzeltme/<str:firma>/<int:pk>/', views.siparisduzeltme, name='siparisduzeltmeurl'),

    path('kargo-ekle/', views.kargoeklemeyap, name='kargoekleurl'),
    path('kargo-exceli-yukle/', views.kargoexceliyuklemeyap, name='kargoexceliyukleurl'),
    path('kargo-listesi/', views.kargolistesiyap, name='kargolistesiurl'),
    path('kargo-listesi/<str:sort>/', views.kargolistesiyap, name='kargosiralamaurl'),
    path('kargo-duzeltme/<str:firma>/<int:pk>/', views.kargoduzeltme, name='kargoduzeltmeurl'),

    path('iade-ekle/', views.iadeeklemeyap, name='iadeekleurl'),
    path('iade-exceli-yukle/', views.iadeexceliyuklemeyap, name='iadeexceliyukleurl'),
    path('iade-listesi/', views.iadelistesiyap, name='iadelistesiurl'),
    path('iade-listesi/<str:sort>/', views.iadelistesiyap, name='iadesiralamaurl'),
    path('iade-duzeltme/<str:firma>/<int:pk>/', views.iadeduzeltme, name='iadeduzeltmeurl'),

    path('gider-ekle/', views.gidereklemeyap, name='giderekleurl'),
    path('gider-exceli-yukle/', views.giderexceliyuklemeyap, name='giderexceliyukleurl'),
    path('gider-listesi/', views.giderlistesiyap, name='giderlistesiurl'),
    path('gider-listesi/<str:sort>/', views.giderlistesiyap, name='gidersiralamaurl'),
    path('gider-detayi/<str:sort>/', views.giderbaslikdetayiyap, name='giderbaslikdetayiurl'),
    path('gider-duzeltme/<str:firma>/<int:pk>/', views.giderduzeltme, name='giderduzeltmeurl'),

    path('kayit-ol/', views.kayitol, name='kayitolurl'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),

    path('stok-exceli-indir/', views.stokexceliindir, name='stokexcelindirurl'),
    path('sayim-exceli-indir/', views.sayimexcelindir, name='sayimexcelindirurl'),
    path('siparis-exceli-indir/', views.sipexceliindir, name='sipexcelindirurl'),
    path('siparis-topla-exceli/<int:sira>', views.siparistoplaexceli, name='siptoplaexcelindirurl'),
    path('kargo-exceli-indir/', views.kargoexceliindir, name='kargoexcelindirurl'),
    path('iade-exceli-indir/', views.iadeexceliindir, name='iadeexcelindirurl'),
    path('gider-exceli-indir/', views.giderexceliindir, name='giderexcelindirurl'),
    
    path('pazaryeri-detayi/<str:pzr>/', views.pazaryeridetayiyap, name='pazaryeridetayurl'),
    path('fatura-detayi/<str:sort>/', views.stokfaturasiyap, name='stokfaturasiurl'),

    path('siparis-yok/', views.siparisyok, name='siparisyokurl'),

    path("robots.txt", TemplateView.as_view(template_name="etikom/robots.txt", content_type="text/plain")),
]