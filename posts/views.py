from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()  # ya viene ordenado por Meta.ordering
    return render(request, "home.html", {"posts": posts})
