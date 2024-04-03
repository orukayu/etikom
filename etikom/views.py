from django.shortcuts import render
from .models import Emutablo
from .forms import CarpmaFormu
from .forms import SayilarFormu
# Create your views here.

def anasayfa(request):
    if request.method == 'POST':
        form = CarpmaFormu(request.POST)
        if form.is_valid():
            sayi1 = form.cleaned_data['sayi1']
            sayi2 = form.cleaned_data['sayi2']
            carpim = sayi1 * sayi2
            return render(request, 'etikom/sonuc.html', {'carpim': carpim})
    else:
        form = CarpmaFormu()
    return render(request, 'etikom/form.html', {'form': form})


def toplama_formu(request):
    form = SayilarFormu(request.POST or None)
    if form.is_valid():
        sayi1 = form.cleaned_data['sayi1']
        sayi2 = form.cleaned_data['sayi2']
        sayi3 = form.cleaned_data['sayi3']
        toplam = sayi1 + sayi2 + sayi3
        return render(request, 'etikom/toplama_formu.html', {'form': form, 'toplam': toplam})
    else:
        return render(request, 'etikom/toplama_formu.html', {'form': form})
