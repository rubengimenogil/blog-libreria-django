from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'posts/index.html', {'posts': posts})

def healthz(request):
    """Health endpoint sin tocar BD (útil para comprobar runtime en Vercel)."""
    return JsonResponse({"ok": True})
