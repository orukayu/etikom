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
    if not request.user.is_authenticated:
        user = authenticate(username='demo firma', password='demofirma')
        if user:
            login(request, user)
            return redirect('demofirmaurl')

    return redirect('demofirmaurl')


def demofirma(request):
    title = 'Etikom'
    baslik = ' İşlemleri'

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
                    return redirect('girisurl')
                else:
                    mesaj = ''
                    giris.add_error('firma_adi', 'Hatalı firma adı veya şifre.')
        elif 'stokekle' in request.POST:
            stok = StokFormu(request.POST)
            if stok.is_valid():
                post = stok.save(commit=False)
                post.Firmaadi = request.user
                post.save1()
                return redirect('demofirmaurl')

        elif 'sipekle' in request.POST:
            siparis = SiparisFormu(request.POST)
            giris = GirisFormu()
            stok = StokFormu()
            if siparis.is_valid():
                post = siparis.save(commit=False)
                post.save3()
                return redirect('demofirmaurl')
        else:
            giris = GirisFormu()
            stok = StokFormu()
            siparis = SiparisFormu()
    else:
        giris = GirisFormu()
        stok = StokFormu()
        siparis = SiparisFormu()

    mesaj = ''
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    stv = Stok.objects.filter(Firmaadi=firma_adi_id).count()                       # Bu kod, Stok modelinde kaç veri olduğunu sayar. Eğer veri yoksa 0 değeri döndürür.

    if stv == 0:                                     # 0 lı şart koyulmazsa tablo boşken hata veriyor.
        ts = 0
        om = 0
        tm = 0
    else:
        ts = Stok.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Adet"))["Adet__sum"]       # Adet sutununda ki rakamlarin toplamini verir.
        tm = Stok.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Toplam"))["Toplam__sum"]
        om = tm / ts

    siv = Siparis.objects.filter(Firmaadi=firma_adi_id).count()                       # Bu kod, Siparis modelinde kaç veri olduğunu sayar. Eğer veri yoksa 0 değeri döndürür.

    if siv == 0:                                     # 0 lı şart koyulmazsa tablo boşken hata veriyor.
        tss = 0
        osm = 0
        tsm = 0
    else:
        tfs = Siparis.objects.filter(Firmaadi=firma_adi_id).values('Siparisno').order_by('Siparisno').distinct()      # Siparis tablosunda ki satir sayisi
        tss = len(tfs)
        tsm = Siparis.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Toplam"))["Toplam__sum"]
        osm = tsm / tss


    return render(request, 'etikom/base.html', {'giris': giris, 'stok': stok, 'siparis': siparis, 'mesaj': mesaj, 'firma_adi': firma_adi, 'baslik': baslik, 'title': title, 'ts': ts, 'om': om, 'tm': tm, 'tss': tss, 'osm': osm, 'tsm': tsm})


def stokliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if sort == 'az-sira-no':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('id').values()
    elif sort == 'za-sira-no':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-id').values()
    elif sort == 'az-fatura-no':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Afaturano').values()
    elif sort == 'za-fatura-no':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Afaturano').values()
    elif sort == 'az-stok-kodu':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Stokkodu').values()
    elif sort == 'za-stok-kodu':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Stokkodu').values()
    elif sort == 'az-adet':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Adet').values()
    elif sort == 'za-adet':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Adet').values()
    elif sort == 'az-alis-fiyati':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Alisfiyati').values()
    elif sort == 'za-alis-fiyati':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Alisfiyati').values()
    elif sort == 'az-toplam':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Toplam').values()
    elif sort == 'za-toplam':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Toplam').values()
    else:
        stok = Stok.objects.filter(Firmaadi=firma_adi_id)

    title = 'Stok Listesi'
    ek = ' Stok Raporu:'
    baslik = firma_adi + ek

    return render(request, 'etikom/stoklistesi.html', {'stok': stok, 'baslik': baslik, 'title': title})


def siparisliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if sort == 'az-sira-no':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('id').values()
    elif sort == 'za-sira-no':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-id').values()
    elif sort == 'az-pazaryeri':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Pazaryeri').values()
    elif sort == 'za-pazaryeri':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Pazaryeri').values()
    elif sort == 'az-tarih':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Tarih').values()
    elif sort == 'za-tarih':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Tarih').values()
    elif sort == 'az-siparis-no':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Siparisno').values()
    elif sort == 'za-siparis-no':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Siparisno').values()
    elif sort == 'az-stok-kodu':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Stokkodu').values()
    elif sort == 'za-stok-kodu':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Stokkodu').values()
    elif sort == 'az-adet':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Adet').values()
    elif sort == 'za-adet':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Adet').values()
    elif sort == 'az-satis-fiyati':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Satisfiyati').values()
    elif sort == 'za-satis-fiyati':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Satisfiyati').values()
    elif sort == 'az-toplam':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Toplam').values()
    elif sort == 'za-toplam':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Toplam').values()
    elif sort == 'az-komisyon-orani':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Komisyon').values()
    elif sort == 'za-komisyon-orani':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Komisyon').values()
    elif sort == 'az-komisyon-tutari':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('Komisyontutari').values()
    elif sort == 'za-komisyon-tutari':
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Komisyontutari').values()
    else:
        siparis = Siparis.objects.filter(Firmaadi=firma_adi_id)

    title = 'Siparis Listesi'
    ek = ' siparis raporu:'
    baslik = firma_adi + ek

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
                    return redirect('demofirmaurl')
            else:
                kayit.add_error('password1', 'Şifre farklı girilmiş.')

    return render(request, 'etikom/kayitol.html', {'baslik':baslik, 'kayit': kayit, 'title': title})



def cikisyap(request):
    logout(request)
    return redirect('anasayfa')


def iletisimyap(request):
    title = 'İletişim'
    baslik = 'İletişim Sayfamız'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/iletisim.html', {'baslik': baslik, 'title': title})

def girisyap(request):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Raporlar'
    ek = ' Rapor Sayfası'
    baslik = firma_adi + ek
    # ... anasayfa içeriğini oluşturun
    return render(request, 'etikom/giris.html', {'baslik': baslik, 'title': title})

def hakkimizdayap(request):
    title = 'Hakkımızda'
    baslik = 'Hakkımızda Sayfamız'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/hakkimizda.html', {'baslik': baslik, 'title': title})

def fiyatlamayap(request):
    title = 'Fiyatlandırma'
    baslik = 'Premium ve Plus Avantajlar'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/fiyatlandirma.html', {'baslik': baslik, 'title': title})

def stokexcelyuklemeyap(request):
    title = 'Excel Yükle'
    baslik = 'Excel ile Stok Yükleme Sayfası'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/stokexcelyukle.html', {'baslik': baslik, 'title': title})

def sipexcelyuklemeyap(request):
    title = 'Excel Yükle'
    baslik = 'Excel ile Sipariş Yükleme Sayfası'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/sipexcelyukle.html', {'baslik': baslik, 'title': title})