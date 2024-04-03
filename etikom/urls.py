from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('toplama_formu/', views.toplama_formu, name='toplama_formu'),
]