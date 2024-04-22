from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('demo-firma/', views.demofirma, name='demofirma'),
    path('demo-firma/stok-listesi/', views.liste, name='stoklistesi'),
    path('demo-firma/stok-listesi/<str:sort>/', views.liste, name='stoksiralama'),
    path('kayit-ol/', views.kayitol, name='kayit-ol'),
    path('cikis-yap/', views.cikisyap, name='cikisurl'),
    path('<firma>/', views.girisyap, name='girisurl'),

]