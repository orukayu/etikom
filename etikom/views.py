from django.shortcuts import render
from .models import Stok
from .forms import PostForm

from django.db.models import Sum

# Create your views here.

def anasayfa(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = PostForm()

    vv = Stok.objects.count() # Bu kod, Stok modelinde kaç veri olduğunu sayar. Eğer veri yoksa 0 değeri döndürür.

    if vv == 0:
        ts = 0
        om = 0
        tm = 0
    else:
        ts = Stok.objects.aggregate(Sum("Adet"))["Adet__sum"]
        tm = Stok.objects.aggregate(Sum("Toplam"))["Toplam__sum"]
        om = tm / ts

    return render(request, 'etikom/a.html', {'form': form, 'ts': ts, 'om': om, 'tm': tm})