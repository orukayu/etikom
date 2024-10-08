from django.urls import path
from . import views
from django.views.generic.base import TemplateView


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

    path('fatura-detayi/<str:sort>/', views.stokfaturasi, name='stokfaturasiurl'),
    path('stok-detayi/<str:sort>/', views.stokgecmisi, name='stokgecmisiurl'),



    path('siparis-ekle/', views.siparisekleme, name='siparisekleurl'),
    path('siparis-exceli-yukle/', views.sipexcelyuklemeyap, name='sipexcelyukleurl'),

    path('siparis-icerikleri/<int:sira>', views.siparistopla, name='siparisleritoplaurl'),
    path('siparis-topla-exceli/<int:sira>', views.siparistoplaexceli, name='siptoplaexcelindirurl'),

    path('siparis-yok/', views.siparisyok, name='siparisyokurl'),

    path('siparis-listesi/', views.siparisliste, name='siparislistesiurl'),
    path('siparis-listesi/<str:sort>/', views.siparisliste, name='siparissiralama'),

    path('siparis-duzeltme/<str:firma>/<int:pk>/', views.siparisduzeltme, name='siparisduzeltmeurl'),
    path('siparis-exceli-indir/', views.sipexceliindir, name='sipexcelindirurl'),

    path('pazaryeri-detayi/<str:pzr>/', views.pazaryeridetay, name='pazaryeridetayurl'),
    path('siparis-detayi/<str:sort>/', views.siparisdetay, name='siparisdetayurl'),



    path('kargo-ekle/', views.kargoeklemeyap, name='kargoekleurl'),
    path('kargo-exceli-yukle/', views.kargoexcelyuklemeyap, name='kargoexcelyukleurl'),

    path('kargo-listesi/', views.kargoliste, name='kargolistesiurl'),
    path('kargo-listesi/<str:sort>/', views.kargoliste, name='kargosiralamaurl'),

    path('kargo-duzeltme/<str:firma>/<int:pk>/', views.kargoduzeltme, name='kargoduzeltmeurl'),
    path('kargo-exceli-indir/', views.kargoexceliindir, name='kargoexcelindirurl'),



    path('iade-ekle/', views.iadeeklemeyap, name='iadeekleurl'),
    path('iade-exceli-yukle/', views.iadeexcelyuklemeyap, name='iadeexcelyukleurl'),

    path('iade-listesi/', views.iadeliste, name='iadelistesiurl'),
    path('iade-listesi/<str:sort>/', views.iadeliste, name='iadesiralamaurl'),
    
    path('iade-duzeltme/<str:firma>/<int:pk>/', views.iadeduzeltme, name='iadeduzeltmeurl'),
    path('iade-exceli-indir/', views.iadeexceliindir, name='iadeexcelindirurl'),




    path('gider-ekle/', views.gidereklemeyap, name='giderekleurl'),
    path('gider-exceli-yukle/', views.giderexcelyuklemeyap, name='giderexcelyukleurl'),

    path('gider-listesi/', views.giderliste, name='giderlistesiurl'),
    path('gider-listesi/<str:sort>/', views.giderliste, name='gidersiralamaurl'),

    path('gider-duzeltme/<str:firma>/<int:pk>/', views.giderduzeltme, name='giderduzeltmeurl'),
    path('gider-exceli-indir/', views.giderexceliindir, name='giderexcelindirurl'),

    path('baslik-detayi/<str:sort>/', views.baslikdetayi, name='baslikdetayiurl'),

    path('giris/', views.girisyap, name='girisurl'),
    path('hakkimizda/', views.hakkimizdayap, name='hakkimizdaurl'),
    path('fiyatlandirma/', views.fiyatlamayap, name='fiyatlamaurl'),
    path('iletisim/', views.iletisimyap, name='iletisimurl'),
    path('blog/', views.blogyap, name='blogurl'),
    path('blog/<str:url>/', views.blogdetayyap, name='blogdetayurl'),
    
    path('kayit-ol/', views.kayitol, name='kayitolurl'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),

    path("robots.txt", TemplateView.as_view(template_name="etikom/robots.txt", content_type="text/plain")),
]