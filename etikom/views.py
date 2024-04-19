from django.shortcuts import render
from django.shortcuts import redirect
from .models import Stok
from .forms import StokForm
from .forms import KayitFormu

from django.db.models import Sum
from django.contrib.auth.models import User


# Create your views here.

def anasayfa(request):
    # ... anasayfa içeriğini oluşturun
    return redirect('demofirma')

def demofirma(request):

    if request.method == "POST":
        kayit = KayitFormu(request.POST)
        form = StokForm(request.POST)

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
        else:
            kayit = KayitFormu()
    else:
        kayit = KayitFormu()


    if request.method == "POST":
        if request.POST.get("stokekle"):
            form = StokForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save1()
                return redirect('demofirma')
        elif request.POST.get("stokcikart"):
            form = StokForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save2()                        # Modelde ki save2 fonksiyonuna git
                return redirect('demofirma')
        else:
            form = StokForm()
    else:
        form = StokForm()

    vv = Stok.objects.count()                       # Bu kod, Stok modelinde kaç veri olduğunu sayar. Eğer veri yoksa 0 değeri döndürür.
    firma_adi = 'DEMO FİRMA'

    if vv == 0:                                     # 0 lı şart koyulmazsa tablo boşken hata veriyor.
        ts = 0
        om = 0
        tm = 0
    else:
        ts = Stok.objects.aggregate(Sum("Adet"))["Adet__sum"]       # Adet sutununda ki rakamlarin toplamini verir.
        tm = Stok.objects.aggregate(Sum("Toplam"))["Toplam__sum"]
        om = tm / ts

    return render(request, 'etikom/base.html', {'firma_adi': firma_adi, 'kayit': kayit, 'form': form, 'ts': ts, 'om': om, 'tm': tm})

def liste(request, sort=None):
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


    return render(request, 'etikom/stoklistesi.html', {'stok': stok})


def kayitol(request):
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

    return render(request, 'etikom/kayitol.html', {'baslik':baslik, 'kayit': kayit})
