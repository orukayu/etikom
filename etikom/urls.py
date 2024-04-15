from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('stoklistesi/', views.liste, name='stoklistesi'),
    path('stoklistesi/<str:sort>/', views.liste, name='stoksiralama'),
]