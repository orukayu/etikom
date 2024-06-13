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
from openpyxl import load_workbook
from openpyxl.styles import numbers
import os
from io import BytesIO
from django.conf import settings

from django.db.models import Min, Max
from dateutil.relativedelta import relativedelta

from django.db.models.functions import ExtractWeek
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear
from datetime import datetime, timedelta
import json


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
            siparis = SiparisFormu(request.POST, user=request.user)
            giris = GirisFormu()
            stok = StokFormu()
            if siparis.is_valid():
                post = siparis.save(commit=False)
                post.Firmaadi = request.user
                post.save3()

                # Stok modeline kaydedilecek verileri ayir
                sipno = siparis.cleaned_data['Siparisno']
                stokkodu = siparis.cleaned_data['Stokkodu']
                sayi = siparis.cleaned_data['Adet']
                adet = sayi * -1
                satfiyat = siparis.cleaned_data['Satisfiyati']
                Firmaadi = request.user

                # Stok modelini olustur ve kaydet
                stok = Stok(Firmaadi=Firmaadi, Afaturano=sipno, Stokkodu=stokkodu, Adet=adet, Alisfiyati=satfiyat)
                stok.save1()
                return redirect('demofirmaurl')
        else:
            giris = GirisFormu()
            stok = StokFormu()
            siparis = SiparisFormu(user=request.user)
    else:
        giris = GirisFormu()
        stok = StokFormu()
        siparis = SiparisFormu(user=request.user)

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


    context = {
        'giris': giris,
        'stok': stok,
        'siparis': siparis,
        'mesaj': mesaj,
        'firma_adi': firma_adi,
        'title': title,
        'ts': ts,
        'om': om,
        'tm': tm,
        'tss': tss,
        'osm': osm,
        'tsm': tsm,
    }

    return render(request, 'etikom/base.html', context)


def stokliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    tfta = Stok.objects.filter(Firmaadi=firma_adi_id).values('Afaturano').order_by('Afaturano').distinct().count()   # toplam fatura sayisi
    tsc = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').order_by('Stokkodu').distinct().count()      # Toplam stok cesidi sayısı

    if tsc == 0:
        tstg = 0
        ksa = 0
        tstm = 0
        ostm = 0
    else:
        tstg = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__gt=0).aggregate(Sum('Adet'))["Adet__sum"]
        ksa = Stok.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Adet"))["Adet__sum"]
        tstm = Stok.objects.filter(Firmaadi=firma_adi_id, Toplam__gt=0).aggregate(Sum("Toplam"))["Toplam__sum"]
        ostm = tstm / tstg

        # None kontrolü
        if tstg is None:
            tstg = 0
            ostm = 0
        if ksa is None:
            ksa = 0
            ostm = 0
        if tstm is None:
            tstm = 0
            ostm = 0

    tstc = abs(ksa - tstg)                                                                                      # Stok cikisi

    if tstc == 0:
        tsatis = 0
    else:
        tsatis = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__lte=0).aggregate(Sum("Toplam"))["Toplam__sum"]          # toplam stok satis bedeli

    tsts = abs(tsatis)

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
    elif sort == 'az-fiyat':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Alisfiyati').values()
    elif sort == 'za-fiyat':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Alisfiyati').values()
    elif sort == 'az-toplam':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('Toplam').values()
    elif sort == 'za-toplam':
        stok = Stok.objects.filter(Firmaadi=firma_adi_id).order_by('-Toplam').values()
    else:
        stok = Stok.objects.filter(Firmaadi=firma_adi_id)

    firma = request.user.username
    title = 'Stok Hareketleri'

    context = {
        'stok': stok,
        'firma_adi': firma_adi,
        'title': title,
        'stsys': stsys,
        'ostm': ostm,
        'tstm': tstm,
        'tsts': tsts,
        'tfta': tfta,
        'tsc': tsc,
        'tstg': tstg,
        'tstc': tstc,
        'ksa': ksa,
        'firma': firma,
    }
    

    return render(request, 'etikom/stoklistesi.html', context)


def siparisliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    tpys = Siparis.objects.filter(Firmaadi=firma_adi_id).values('Pazaryeri').order_by('Pazaryeri').distinct().count()
    tsps = Siparis.objects.filter(Firmaadi=firma_adi_id).values('Siparisno').order_by('Siparisno').distinct().count()
    tsts = Siparis.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').order_by('Stokkodu').distinct().count()
    tstc = Siparis.objects.filter(Firmaadi=firma_adi_id, Adet__gt=0).aggregate(Sum('Adet'))["Adet__sum"]

    if tstc is None:
        tstc = 0

    # En küçük ve en büyük tarihleri bulma
    tarih_araligi = Siparis.objects.filter(Firmaadi=firma_adi_id).aggregate(en_kucuk_tarih=Min('Tarih'), en_buyuk_tarih=Max('Tarih'))

    en_kucuk_tarih = tarih_araligi['en_kucuk_tarih']
    en_buyuk_tarih = tarih_araligi['en_buyuk_tarih']

    # Tarihler arasındaki farkı hesaplama
    if en_buyuk_tarih and en_kucuk_tarih:
        fark = relativedelta(en_buyuk_tarih, en_kucuk_tarih)
        fark_ay = fark.years * 12 + fark.months
        if fark_ay == 0:
            tdns = 1
        elif fark_ay == None:
            tdns = 0
        else:
            tdns = fark_ay + 1
    else:
        tdns = 0

    if tstc == 0:
        orsp = 0
    else:
        orsp = tstc / tsps

    tstt = Siparis.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Toplam"))["Toplam__sum"]

    if tstt is None:
        tstt = 0
        ostt = 0
    else:
        ostt = tstt / tsps

    stsys = Siparis.objects.filter(Firmaadi=firma_adi_id).count()

    if sort == 'az-pazaryeri':
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

    firma = request.user.username
    title = 'Sipariş Hareketleri'

    context = {
        'siparis': siparis,
        'firma_adi': firma_adi,
        'title': title,
        'tpys': tpys,
        'tsps': tsps,
        'tsts': tsts,
        'tstc': tstc,
        'tdns': tdns,
        'orsp': orsp,
        'tstt': tstt,
        'ostt': ostt,
        'stsys': stsys,
        'firma': firma,
    }

    return render(request, 'etikom/siparislistesi.html', context)

def girisyap(request):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    title = 'Raporlar'    

    kont_tststt = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__lte=0).aggregate(Sum("Toplam"))["Toplam__sum"]
    if kont_tststt == None:
        tststt = 0
    else:
        tststt = abs(kont_tststt)

    kont_tsistt = Siparis.objects.filter(Firmaadi=firma_adi_id).aggregate(Sum("Toplam"))["Toplam__sum"]
    if kont_tsistt == None:
        tsistt = 0
    else:
        tsistt = abs(kont_tsistt)

    ts = tststt + tsistt

    # En küçük ve en büyük tarihleri bulma
    tarih_araligi = Siparis.objects.filter(Firmaadi=firma_adi_id).aggregate(en_kucuk_tarih=Min('Tarih'), en_buyuk_tarih=Max('Tarih'))

    en_kucuk_tarih = tarih_araligi['en_kucuk_tarih']
    en_buyuk_tarih = tarih_araligi['en_buyuk_tarih']

    # Tarihler arasındaki farkı hesaplama
    if en_buyuk_tarih and en_kucuk_tarih:
        fark = relativedelta(en_buyuk_tarih, en_kucuk_tarih)
        fark_ay = fark.years * 12 + fark.months
        if fark_ay == 0:
            tdns = 1
        elif fark_ay == None:
            tdns = 0
        else:
            tdns = fark_ay + 1
    else:
        tdns = 0


    # Şu anki tarih
    today = datetime.today()

    # Son 6 ay
    six_months_ago = today - timedelta(days=6*30)
    # Son 2 yıl
    two_years_ago = today - timedelta(days=2*365)

    # Son 6 ayın haftalık satışları
    weekly_sales = Siparis.objects.filter(Firmaadi=firma_adi_id, Tarih__gte=six_months_ago).annotate(
        week=ExtractWeek('Tarih')
    ).values('week').annotate(total=Sum('Toplam')).order_by('week')
    weeks = [entry['week'] for entry in weekly_sales]
    weekly_totals = [float(entry['total']) for entry in weekly_sales]

    # Son 2 yılın aylık satışları
    monthly_sales = Siparis.objects.filter(Firmaadi=firma_adi_id, Tarih__gte=two_years_ago).annotate(
        year=ExtractYear('Tarih'),
        month=ExtractMonth('Tarih')
    ).values('year', 'month').annotate(total=Sum('Toplam')).order_by('year', 'month')
    months = [f"{entry['year']}-{entry['month']:02d}" for entry in monthly_sales]
    monthly_totals = [float(entry['total']) for entry in monthly_sales]

    context = {
        'weeks': json.dumps(weeks),
        'weekly_totals': json.dumps(weekly_totals),
        'months': json.dumps(months),
        'monthly_totals': json.dumps(monthly_totals),
        'title': title,
        'firma_adi': firma_adi,
        'tdns': tdns,
        'tsistt': tsistt,
        'tststt': tststt,
        'ts': ts,
    }

    return render(request, 'etikom/giris.html', context)

def kayitol(request):
    title = 'Kayıt Ol'
    kayit = KayitFormu()
    firma_adi = request.user.username
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

    return render(request, 'etikom/kayitol.html', {'firma_adi': firma_adi, 'kayit': kayit, 'title': title})



def cikisyap(request):
    logout(request)
    return redirect('anasayfa')


def iletisimyap(request):
    firma_adi = request.user.username
    title = 'İletişim'
    # ... iletişim sayfası içeriğini oluşturun
    return render(request, 'etikom/iletisim.html', {'title': title, 'firma_adi': firma_adi})

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
                stok.save1()
            
            return redirect('stoklistesiurl')

    return render(request, 'etikom/stokexcelyukle.html', {'firma_adi': firma_adi, 'title': title})


def sipexcelyuklemeyap(request):
    title = 'Excel Yükle'
    firma_adi = request.user.username

    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                sip = Siparis(
                    Pazaryeri = row['Pazaryeri'],
                    Tarih = row['Sipariş Tarihi'],
                    Siparisno = row['Sipariş No'],
                    Stokkodu = row['Stok Kodu'],
                    Adet = row['Adet'],
                    Satisfiyati = row['Satış Fiyatı'],
                    Komisyon = row['Komisyon (%)'],
                    Firmaadi = request.user
                )
                sip.save3()
                stk = Stok(
                    Firmaadi = request.user,
                    Afaturano = row['Sipariş No'],
                    Stokkodu = row['Stok Kodu'],
                    Adet = row['Adet'] * -1,
                    Alisfiyati = row['Satış Fiyatı'],
                )
                stk.save1()

            return redirect('siparislistesiurl')
    
    return render(request, 'etikom/sipexcelyukle.html', {'firma_adi': firma_adi, 'title': title})


def stokexceliindir(request):
    firma_adi_id = request.user.id

    # Stok modelinden tüm verileri al
    stoklar = Stok.objects.filter(Firmaadi=firma_adi_id)

    # Stok verilerini bir DataFrame'e dönüştür
    data = {
        'Belge No': [stok.Afaturano for stok in stoklar],
        'Stok Kodu': [stok.Stokkodu for stok in stoklar],
        'Adet': [stok.Adet for stok in stoklar],
        'Fiyat': [str(stok.Alisfiyati).replace('.', ',') for stok in stoklar],
        'Toplam': [str(stok.Toplam).replace('.', ',') for stok in stoklar],
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



def stokduzeltme(request, firma, pk):
    
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if firma_adi != firma:
        return redirect('demofirmaurl')

    fa = firma
    pk = pk

    sipbncek = Stok.objects.filter(id=pk).values_list('Afaturano', flat=True).first()
    sipvarmi = Siparis.objects.filter(Firmaadi=firma_adi_id, Siparisno=sipbncek).exists()
    
    if not sipvarmi:
        kontrolstok = get_object_or_404(Stok, pk=pk)

        if request.method == "POST":
            form = StokFormu(request.POST, instance=kontrolstok)
            if 'stoksil' in request.POST:
                kontrolstok.delete()
                return redirect('stoklistesiurl')
            elif 'stokekle' in request.POST:
                if form.is_valid():
                    post = form.save(commit=False)
                    post.Firmaadi = request.user
                    post.save1()
                    return redirect('stoklistesiurl')
        else:
            form = StokFormu(instance=kontrolstok)
    else:
        sk = Stok.objects.filter(id=pk).values_list('Stokkodu', flat=True).first()
        pk = Siparis.objects.filter(Firmaadi=firma_adi_id, Siparisno=sipbncek, Stokkodu=sk).values_list('id', flat=True).first()

        return redirect('siparisduzeltmeurl', firma, pk)

    title = 'Stok Detayı'
    form = StokFormu(instance=kontrolstok)
    return render(request, 'etikom/stokdetay.html', {'form': form, 'firma_adi': firma_adi, 'title': title})


def sayimliste(request, sort=None):
    firma_adi = request.user.username
    firma_adi_id = request.user.id

    # Adet > 0 olan satırlardan Toplam sütunlarının toplamını hesaplama
    toplam_toplam = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__gt=0).values('Stokkodu').annotate(
        total_toplam=Sum('Toplam')
    ).order_by('Stokkodu')

    # Adet > 0 olan satırlardan Adet sütunlarının toplamını hesaplama
    toplam_adet_filtered = Stok.objects.filter(Firmaadi=firma_adi_id, Adet__gt=0).values('Stokkodu').annotate(
        total_adet_filtered=Sum('Adet')
    ).order_by('Stokkodu')

    # Stok Kodu'na göre tüm Adet sütunlarının toplamını hesaplama (Adet değerine bakmaksızın)
    toplam_adet_all = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(
        total_adet_all=Sum('Adet')
    ).order_by('Stokkodu')

    # Sonuçları birleştirerek tek bir yapı oluşturma
    etopla = {}
    for item in toplam_toplam:
        etopla[item['Stokkodu']] = {
            'total_toplam': item['total_toplam'],
            'total_adet_filtered': 0,
            'total_adet_all': 0,
            'ortalama_alisfiyati': 0
        }

    for item in toplam_adet_filtered:
        if item['Stokkodu'] in etopla:
            etopla[item['Stokkodu']]['total_adet_filtered'] = item['total_adet_filtered']

    for item in toplam_adet_all:
        if item['Stokkodu'] in etopla:
            etopla[item['Stokkodu']]['total_adet_all'] = item['total_adet_all']

    # Ortalama alış fiyatını hesaplama
    for stok_kodu, values in etopla.items():
        total_toplam = values['total_toplam']
        total_adet_filtered = values['total_adet_filtered']
        values['ortalama_alisfiyati'] = total_toplam / total_adet_filtered if total_adet_filtered else 0


    # stsys = etopla.count()
    title = 'Stok Listesi'

    context = {
        'etopla': etopla,
        'firma_adi': firma_adi,
        'title': title,
    }

    return render(request, 'etikom/sayimlistesi.html', context)


def sayimexcelindir(request):
    firma_adi_id = request.user.id

    # Stok modelinden tüm verileri al
    stoklar = Stok.objects.filter(Firmaadi=firma_adi_id).values('Stokkodu').annotate(total_adet=Sum('Adet'))

    # Stok verilerini bir DataFrame'e dönüştür
    data = {
        'Stok Kodu': [item['Stokkodu'] for item in stoklar],
        'Mevcut Adet': [item['total_adet'] for item in stoklar],
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


def stokeklemeyap(request):

    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if request.method == "POST":
        if 'stokekle' in request.POST:
            form = StokFormu(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.Firmaadi = request.user
                post.save1()
                return redirect('stoklistesiurl')

    else:
        form = StokFormu()

    title = 'Stok Ekle'
    
    return render(request, 'etikom/stokekle.html', {'form': form, 'firma_adi': firma_adi, 'title': title})


def siparisekleme(request):

    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if request.method == "POST":
        if 'sipekle' in request.POST:
            siparis = SiparisFormu(request.POST, user=request.user)
            if siparis.is_valid():
                post = siparis.save(commit=False)
                post.Firmaadi = request.user
                post.save3()

                sipno = siparis.cleaned_data['Siparisno']
                stokkodu = siparis.cleaned_data['Stokkodu']
                sayi = siparis.cleaned_data['Adet']
                adet = sayi * -1
                satfiyat = siparis.cleaned_data['Satisfiyati']
                Firmaadi = request.user

                # Book kaydet
                stok = Stok(Firmaadi=Firmaadi, Afaturano=sipno, Stokkodu=stokkodu, Adet=adet, Alisfiyati=satfiyat)
                stok.save1()
                return redirect('siparislistesiurl')

    else:
        siparis = SiparisFormu(user=request.user)

    title = 'Sipariş Ekle'
    
    return render(request, 'etikom/sipekle.html', {'siparis': siparis, 'firma_adi': firma_adi, 'title': title})


def stokfaturasi(request, sort):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Fatura Detayı'
    fatura = Stok.objects.filter(Firmaadi=firma_adi_id, Afaturano=sort)

    tstc = Stok.objects.filter(Firmaadi=firma_adi_id, Afaturano=sort).values('Stokkodu').order_by('Stokkodu').distinct().count()
    tsta = Stok.objects.filter(Firmaadi=firma_adi_id, Afaturano=sort).aggregate(Sum("Adet"))["Adet__sum"]

    if tsta <= 0:
        tip = 'ile Satış'
    else:
        tip = 'ile Alım'
    
    tsta = abs(tsta)

    sftt = Stok.objects.filter(Firmaadi=firma_adi_id, Afaturano=sort).aggregate(Sum("Toplam"))["Toplam__sum"]

    sftt = abs(sftt)

    oafi = sftt / tsta

    context = {
        'firma_adi': firma_adi,
        'title': title,
        'sort': sort,
        'fatura': fatura,
        'tstc': tstc,
        'tsta': tsta,
        'sftt': sftt,
        'tip': tip,
        'oafi': oafi,
    }

    return render(request, 'etikom/stokfaturasi.html', context)



def stokgecmisi(request, sort):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Stok Geçmişi'

    stok = Stok.objects.filter(Firmaadi=firma_adi_id, Stokkodu=sort)
    
    ma = Stok.objects.filter(Firmaadi=firma_adi_id, Stokkodu=sort).aggregate(Sum("Adet"))["Adet__sum"]
    tstc = Stok.objects.filter(Firmaadi=firma_adi_id, Stokkodu=sort, Adet__lte=0).aggregate(Sum("Adet"))["Adet__sum"]
    
    if tstc == None:
        tstc = 0
    else:
        tstc = abs(tstc)

    tsaf = Stok.objects.filter(Firmaadi=firma_adi_id, Stokkodu=sort, Adet__gt=0).aggregate(Sum("Toplam"))["Toplam__sum"]
    soaf = tsaf / (ma + tstc)

    tssf = Stok.objects.filter(Firmaadi=firma_adi_id, Stokkodu=sort, Adet__lte=0).aggregate(Sum("Toplam"))["Toplam__sum"]
    if tssf == None:
        tssf = 0

    if tstc != 0:
        sosf = tssf / tstc
        sosf = abs(sosf)
    else:
        sosf = 0

    context = {
        'firma_adi': firma_adi,
        'title': title,
        'sort': sort,
        'stok': stok,
        'ma': ma,
        'tstc': tstc,
        'soaf': soaf,
        'sosf': sosf,
    }

    return render(request, 'etikom/stokgecmisi.html', context)

def siparisduzeltme(request, firma, pk):

    firma_adi = request.user.username
    firma_adi_id = request.user.id

    if firma_adi != firma:
        return redirect('demofirmaurl')

    kontrol = get_object_or_404(Siparis, pk=pk)
    siparis = SiparisFormu(instance=kontrol, user=request.user)

    sinca = Siparis.objects.filter(id=pk).values_list('Siparisno', flat=True).first()
    stkca = Siparis.objects.filter(id=pk).values_list('Stokkodu', flat=True).first()
    kstok = get_object_or_404(Stok, Afaturano=sinca, Stokkodu=stkca)

    if request.method == "POST":
        if 'siparissil' in request.POST:
            kontrol.delete()
            kstok.delete()
            return redirect('siparislistesiurl')
        elif 'siparisekle' in request.POST:
            siparis = SiparisFormu(request.POST, instance=kontrol, user=request.user)
            if siparis.is_valid():
                post = siparis.save(commit=False)
                post.Firmaadi = request.user
                post.save3()

                sipno = siparis.cleaned_data['Siparisno']
                stokkodu = siparis.cleaned_data['Stokkodu']
                sayi = siparis.cleaned_data['Adet']
                adet = sayi * -1
                satfiyat = siparis.cleaned_data['Satisfiyati']
                
                kstok.Firmaadi = request.user
                kstok.Afaturano = sipno
                kstok.Stokkodu = stokkodu
                kstok.Adet = adet
                kstok.Alisfiyati = satfiyat
                kstok.save1()

                return redirect('siparislistesiurl')

    title = 'Sipariş Detayı'
    return render(request, 'etikom/siparisdetay.html', {'siparis': siparis, 'firma_adi': firma_adi, 'title': title})


def sipexceliindir(request):
    firma_adi_id = request.user.id

    # Siparis modelinden tüm verileri al
    sipler = Siparis.objects.filter(Firmaadi=firma_adi_id)

    # Siparis verilerini bir DataFrame'e dönüştür
    data = {
        'Pazaryeri': [siparis.Pazaryeri for siparis in sipler],
        'Tarih': [siparis.Tarih.strftime('%d.%m.%Y') for siparis in sipler],
        'Sipariş No': [siparis.Siparisno for siparis in sipler],
        'Stok Kodu': [siparis.Stokkodu for siparis in sipler],
        'Adet': [str(siparis.Adet).replace('.', ',') for siparis in sipler],
        'Satış Fiyatı': [str(siparis.Satisfiyati).replace('.', ',') for siparis in sipler],
        'Toplam': [str(siparis.Toplam).replace('.', ',') for siparis in sipler],
        'Komisyon %': [str(siparis.Komisyon).replace('.', ',') for siparis in sipler],
        'Komisyon Tutarı': [str(siparis.Komisyontutari).replace('.', ',') for siparis in sipler],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Siparisler')
    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_etikom_siparisler.xlsx"'

    return response


def pazaryeridetay(request, pzr):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Pazaryeri Detayı'

    pazaryeri = Siparis.objects.filter(Firmaadi=firma_adi_id, Pazaryeri=pzr)

    tstc = Siparis.objects.filter(Firmaadi=firma_adi_id, Pazaryeri=pzr).values('Stokkodu').order_by('Stokkodu').distinct().count()
    tsta = Siparis.objects.filter(Firmaadi=firma_adi_id, Pazaryeri=pzr).aggregate(Sum("Adet"))["Adet__sum"]
    
    tsta = abs(tsta)

    sftt = Siparis.objects.filter(Firmaadi=firma_adi_id, Pazaryeri=pzr).aggregate(Sum("Toplam"))["Toplam__sum"]

    sftt = abs(sftt)

    oafi = sftt / tsta

    context = {
        'firma_adi': firma_adi,
        'title': title,
        'pazaryeri': pazaryeri,
        'tstc': tstc,
        'tsta': tsta,
        'sftt': sftt,
        'oafi': oafi,
        'pzr': pzr,
    }

    return render(request, 'etikom/pazaryeridetay.html', context)

def siparistopla(request, sira):
    firma_adi = request.user.username
    firma_adi_id = request.user.id
    title = 'Siparişler'

    tarihler = list(Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Tarih').values_list('Tarih', flat=True).distinct())
    en_son_tarih = tarihler[sira-1]

    liste_sayisi = len(tarihler)

    if en_son_tarih is not None:
        # En son tarihe ait siparişleri filtreleyin
        en_son_sipler = Siparis.objects.filter(Firmaadi=firma_adi_id, Tarih=en_son_tarih)
        
        # Stok kodlarını ve adet toplamlarını gruplayın ve hesaplayın
        stok_toplamlari = en_son_sipler.values('Stokkodu').annotate(total_quantity=Sum('Adet'))
    else:
        stok_toplamlari = []

    context = {
        'firma_adi': firma_adi,
        'title': title,
        'en_son_tarih': en_son_tarih,
        'stok_toplamlari': stok_toplamlari,
        'sira': sira,
        'liste_sayisi': liste_sayisi,
    }

    return render(request, 'etikom/siparistopla.html', context)


def siparistoplaexceli(request, sira):
    firma_adi_id = request.user.id

    # Tarihleri sıralı ve benzersiz hale getirin
    tarihler = list(Siparis.objects.filter(Firmaadi=firma_adi_id).order_by('-Tarih').values_list('Tarih', flat=True).distinct())
    en_son_tarih = tarihler[sira-1]

    sipler = Siparis.objects.filter(Firmaadi=firma_adi_id, Tarih=en_son_tarih)
    stok_toplamlari = sipler.values('Stokkodu').annotate(total_quantity=Sum('Adet'))

    # Siparis verilerini bir DataFrame'e dönüştür
    data = {
        'Stok Kodu': [stok['Stokkodu'] for stok in stok_toplamlari],
        'Toplam Adet': [stok['total_quantity'] for stok in stok_toplamlari],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sayfa1')
    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_etikom_{en_son_tarih}_sevkiyat.xlsx"'

    return response