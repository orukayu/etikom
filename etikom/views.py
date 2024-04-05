from django.shortcuts import render
from .models import Stok
from .forms import PostForm

# Create your views here.

def anasayfa(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = PostForm()

    return render(request, 'etikom/a.html', {'form': form})
