from django.shortcuts import render, get_object_or_404
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

import pandas as pd         # pip install pandas ile excel yukleme icin pandas kuruldu ve pd kisaltma adi verildi, ayrıca pip install openpyxl ında kurulması gerekıyor.
from django.http import HttpResponse
import os
from io import BytesIO
from django.conf import settings


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
    baslik = 'İşlemleri'

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

    tfta = Stok.objects.filter(Firmaadi=firma_adi_id).values('Afaturano').order_by('Afaturano').distinct().count()
    tsc = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').order_by('Stokkodu').distinct().count()
    tstg = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__gt=0).aggregate(Sum('Adet'))["Adet__sum"]   #firma id si giriş yapılan firmanın olan ve Adet sütunu 0 dan büyük olan satırların toplamı
    ksa = Stok.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Adet"))["Adet__sum"]
    tstc = (ksa - tstg) * (-1)
    tstm = Stok.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Toplam"))["Toplam__sum"]
    ostm = tstm / ksa

    stsys = Stok.objects.filter(Firmaadi=firma_adi_id).count()

    if sort == 'az-fatura-no':
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

    title = 'Stok Hareketleri'
    

    return render(request, 'etikom/stoklistesi.html', {'stsys': stsys, 'stok': stok, 'firma_adi': firma_adi, 'title': title, 'tfta': tfta, 'tsc': tsc, 'tstg': tstg, 'tstc': tstc, 'ksa': ksa, 'tstm': tstm, 'ostm': ostm})


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

    title = 'Sipariş Listesi'
    ek = ' sipariş raporu:'
    baslik = firma_adi + ek

    return render(request, 'etikom/siparislistesi.html', {'siparis': siparis, 'baslik': baslik, 'title': title})



def kayitol(request):
    title = 'Kayıt Ol'
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

    return render(request, 'etikom/kayitol.html', {'kayit': kayit, 'title': title})



def cikisyap(request):
    logout(request)
    return redirect('anasayfa')


def iletisimyap(request):
    firma_adi = request.user.username
    title = 'İletişim'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/iletisim.html', {'title': title, 'firma_adi': firma_adi})

def girisyap(request):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Raporlar'
    baslik = ' Rapor Sayfası'
    # ... anasayfa içeriğini oluşturun
    return render(request, 'etikom/giris.html', {'baslik': baslik, 'title': title, 'firma_adi': firma_adi})

def hakkimizdayap(request):
    firma_adi = request.user.username
    title = 'Hakkımızda'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/hakkimizda.html', {'title': title, 'firma_adi': firma_adi})

def fiyatlamayap(request):
    firma_adi = request.user.username
    title = 'Fiyatlandırma'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/fiyatlandirma.html', {'title': title, 'firma_adi': firma_adi})

def stokexcelyuklemeyap(request):
    title = 'Excel Yükle'
    firma_adi = request.user.username

    # ... iletişim sayfası içeriğini oluşturun
    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                stok = Stok(
                    Afaturano = row['Fatura No'],
                    Stokkodu = row['Stok Kodu'],
                    Adet = row['Adet'],
                    Alisfiyati = row['Fiyat'],
                    Toplam = row['Toplam'],
                    Firmaadi = request.user
                )
                stok.save()
            
            return redirect('stoklistesiurl')

    return render(request, 'etikom/stokexcelyukle.html', {'firma_adi': firma_adi, 'title': title})


def sipexcelyuklemeyap(request):
    title = 'Excel Yükle'
    baslik = 'Excel ile Sipariş Yükleme Sayfası'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/sipexcelyukle.html', {'baslik': baslik, 'title': title})


def stokexceliindir(request):
    firma_adi_id = request.user.id

    # Stok modelinden tüm verileri al
    stoklar = Stok.objects.filter(Firmaadi=firma_adi_id)

    # Stok verilerini bir DataFrame'e dönüştür
    data = {
        'Fatura No': [stok.Afaturano for stok in stoklar],
        'Stok Kodu': [stok.Stokkodu for stok in stoklar],
        'Adet': [stok.Adet for stok in stoklar],
        'Alış Fiyatı': [stok.Alisfiyati for stok in stoklar],
        'Toplam': [stok.Toplam for stok in stoklar],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_etikom_stok_hareketleri.xlsx"'

    return response



def stokduzeltme(request):

    firma_adi = request.user.username
    firma_adi_id = request.user.id

    pk = request.POST.get('pk')
    kontrol = get_object_or_404(Stok, pk=pk)
    form = StokFormu(instance=kontrol)

    if request.method == "POST":
        if 'stoksil' in request.POST:
            kontrol.delete()
            return redirect('stoklistesiurl')
        elif 'stokekle' in request.POST:
            form = StokFormu(request.POST, instance=kontrol)
            if form.is_valid():
                post = form.save(commit=False)
                post.Firmaadi = request.user
                post.save1()
                return redirect('stoklistesiurl')

    else:
        form = StokFormu(instance=kontrol)

    title = 'Stok Detayı'
    
    return render(request, 'etikom/stokdetay.html', {'form': form, 'firma_adi': firma_adi, 'title': title})


def sayimliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    # Stokkodu ile gruplandırma ve Adet sütununun toplamını hesaplama
    etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet')).order_by('Stokkodu')

    if sort == 'az-stok-kodu':
        etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet')).order_by('Stokkodu').values()
    elif sort == 'za-stok-kodu':
        etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet')).order_by('-Stokkodu').values()
    elif sort == 'az-adet':
        etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Adet').annotate(total_adet=Sum('Adet')).order_by('Adet').values()
    elif sort == 'za-adet':
        etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Adet').annotate(total_adet=Sum('Adet')).order_by('-Adet').values()
    else:
        etopla = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet')).order_by('Stokkodu')

    stsys = etopla.count()
    title = 'Stok Listesi'

    context = {
        'etopla': etopla,
        'firma_adi': firma_adi,
        'title': title,
        'stsys': stsys,
    }

    return render(request, 'etikom/sayimlistesi.html', context)


def sayimexcelindir(request):
    firma_adi_id = request.user.id

    # Stok modelinden tüm verileri al
    stoklar = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet'))

    # Stok verilerini bir DataFrame'e dönüştür
    data = {
        'Stok Kodu': [item['Stokkodu'] for item in stoklar],
        'Adet': [item['total_adet'] for item in stoklar],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_etikom_stok_adetleri.xlsx"'

    return response