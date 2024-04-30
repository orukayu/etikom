from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from .models import Stok
from .models import Siparis
from .forms import StokFormu
from .forms import KayitFormu
from .forms import GirisFormu
from .forms import SiparisFormu

from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Create your views here.

def anasayfa(request):
    # ... anasayfa içeriğini oluşturun
    return redirect('demofirma')


def demofirma(request):

    if request.method == 'POST':
        if 'girisyap' in request.POST:
            giris = GirisFormu(request.POST)
            stok = StokFormu()
            siparis = SiparisFormu()
            if giris.is_valid():
                firma_adi = giris.cleaned_data['firma_adi']
                password1 = giris.cleaned_data['password1']
                userkontrol = authenticate(username=firma_adi, password=password1)
                if userkontrol is not None:
                    login(request, userkontrol)
                    firma = userkontrol.username
                    # Kullanıcıyı URL'ye yönlendir ve urlde kullanilacak olan bilgiyide tasi
                    return redirect('girisurl', firma)
                else:
                    mesaj = ''
                    giris.add_error('firma_adi', 'Hatalı firma adı veya şifre.')
        elif 'stokekle' in request.POST:
            stok = StokFormu(request.POST)
            if stok.is_valid():
                post = stok.save(commit=False)
                post.save1()
                return redirect('demofirma')
        elif 'stokcikart' in request.POST:
            stok = StokFormu(request.POST)
            if stok.is_valid():
                post = stok.save(commit=False)
                post.save2()
                return redirect('demofirma')
        elif 'sipekle' in request.POST:
            siparis = SiparisFormu(request.POST)
            giris = GirisFormu()
            stok = StokFormu()
            if siparis.is_valid():
                post = siparis.save(commit=False)
                post.save3()
                return redirect('demofirma')
        else:
            giris = GirisFormu()
            stok = StokFormu()
            siparis = SiparisFormu()
    else:
        giris = GirisFormu()
        stok = StokFormu()
        siparis = SiparisFormu()

    vv = Stok.objects.count()                       # Bu kod, Stok modelinde kaç veri olduğunu sayar. Eğer veri yoksa 0 değeri döndürür.
    mesaj = ''
    firma_adi = 'Demo Firma Kontrol Paneli'
    title = 'Etikom'

    if vv == 0:                                     # 0 lı şart koyulmazsa tablo boşken hata veriyor.
        ts = 0
        om = 0
        tm = 0
    else:
        ts = Stok.objects.aggregate(Sum("Adet"))["Adet__sum"]       # Adet sutununda ki rakamlarin toplamini verir.
        tm = Stok.objects.aggregate(Sum("Toplam"))["Toplam__sum"]
        om = tm / ts

    return render(request, 'etikom/base.html', {'giris': giris, 'stok': stok, 'siparis': siparis, 'mesaj': mesaj, 'firma_adi': firma_adi, 'title': title, 'ts': ts, 'om': om, 'tm': tm})


def stokliste(request, sort=None):
    stok = Stok.objects.all()

    if sort == 'az-faturano':
        stok = Stok.objects.all().order_by('Afaturano').values()
    elif sort == 'za-faturano':
        stok = Stok.objects.all().order_by('-Afaturano').values()
    elif sort == 'az-stokkodu':
        stok = Stok.objects.all().order_by('Stokkodu').values()
    elif sort == 'za-stokkodu':
        stok = Stok.objects.all().order_by('-Stokkodu').values()
    elif sort == 'az-adet':
        stok = Stok.objects.all().order_by('Adet').values()
    elif sort == 'za-adet':
        stok = Stok.objects.all().order_by('-Adet').values()
    elif sort == 'az-alisfiyati':
        stok = Stok.objects.all().order_by('Alisfiyati').values()
    elif sort == 'za-alisfiyati':
        stok = Stok.objects.all().order_by('-Alisfiyati').values()
    elif sort == 'az-toplam':
        stok = Stok.objects.all().order_by('Toplam').values()
    elif sort == 'za-toplam':
        stok = Stok.objects.all().order_by('-Toplam').values()
    else:
        stok = Stok.objects.all()

    baslik = 'Sayfa Özeti:'
    title = 'Stok Listesi'

    return render(request, 'etikom/stoklistesi.html', {'stok': stok, 'baslik': baslik, 'title': title})


def siparisliste(request, sort=None):
    siparis = Siparis.objects.all()

    if sort == 'az-faturano':
        stok = Stok.objects.all().order_by('Afaturano').values()
    elif sort == 'za-faturano':
        stok = Stok.objects.all().order_by('-Afaturano').values()
    elif sort == 'az-stokkodu':
        stok = Stok.objects.all().order_by('Stokkodu').values()
    elif sort == 'za-stokkodu':
        stok = Stok.objects.all().order_by('-Stokkodu').values()
    elif sort == 'az-adet':
        stok = Stok.objects.all().order_by('Adet').values()
    elif sort == 'za-adet':
        stok = Stok.objects.all().order_by('-Adet').values()
    elif sort == 'az-alisfiyati':
        stok = Stok.objects.all().order_by('Alisfiyati').values()
    elif sort == 'za-alisfiyati':
        stok = Stok.objects.all().order_by('-Alisfiyati').values()
    elif sort == 'az-toplam':
        stok = Stok.objects.all().order_by('Toplam').values()
    elif sort == 'za-toplam':
        stok = Stok.objects.all().order_by('-Toplam').values()
    else:
        stok = Stok.objects.all()

    baslik = 'Sayfa Özeti:'
    title = 'Siparis Listesi'

    return render(request, 'etikom/siparislistesi.html', {'siparis': siparis, 'baslik': baslik, 'title': title})



def kayitol(request):
    title = 'Kayıt Ol'
    baslik = 'Kayıt Sayfasına Hoşgeldiniz'
    kayit = KayitFormu()
    if request.method == "POST":
        kayit = KayitFormu(request.POST)

        firma_adi = request.POST["firma_adi"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if kayit.is_valid():
            if password1 == password2:
                var = User.objects.filter(username=firma_adi).count()
                if var > 0:
                    kayit.add_error('firma_adi', 'Bu firma adı zaten kullanılıyor.')
                else:
                    kayit = User.objects.create_user(username=firma_adi, email=email, password=password1)
                    kayit.save()
                    return redirect('demofirma')
            else:
                kayit.add_error('password1', 'Şifre farklı girilmiş.')

    return render(request, 'etikom/kayitol.html', {'baslik':baslik, 'kayit': kayit, 'title': title})



def cikisyap(request):
    logout(request)
    return redirect('demofirma')


def iletisimyap(request):
    title = 'İletişim'
    baslik = 'İletişim Sayfamız'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/iletisim.html', {'baslik': baslik, 'title': title})

def girisyap(request, firma):
    #firma = GirisFormu(request.POST)
    # ... anasayfa içeriğini oluşturun
    return render(request, 'etikom/a.html', {})

def hakkimizdayap(request):
    title = 'Hakkımızda'
    baslik = 'Hakkımızda Sayfamız'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/hakkimizda.html', {'baslik': baslik, 'title': title})

def fiyatlamayap(request):
    title = 'Fiyatlandırma'
    baslik = 'Paket Sayfamız'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/fiyatlandirma.html', {'baslik': baslik, 'title': title})