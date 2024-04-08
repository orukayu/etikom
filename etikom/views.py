from django.shortcuts import render
from .models import Stok
from .forms import PostForm

from django.db.models import Sum, Avg

# Create your views here.

def anasayfa(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = PostForm()

    ts = Stok.objects.aggregate(Sum("Adet"))
    tm = Stok.objects.aggregate(Sum("Toplam"))
    om = tm["Toplam__sum"] / ts["Adet__sum"]
    return render(request, 'etikom/a.html', {'form': form, 'ts': ts, 'om': om, 'tm': tm})
