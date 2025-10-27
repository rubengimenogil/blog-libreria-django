from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'posts/index.html', {'posts': posts})

def healthz(request):
    """Health endpoint sin tocar BD (útil para comprobar runtime en Vercel)."""
    return JsonResponse({"ok": True})

def db_healthz(request):
    """Comprueba conectividad a la base de datos ejecutando SELECT 1.

    Devuelve 200 si la conexión funciona; 500 si hay error de conexión/SSL/credenciales.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
        return JsonResponse({"ok": True, "db": True, "result": row[0] if row else None})
    except Exception as exc:
        return JsonResponse({"ok": False, "db": False, "error": str(exc)}, status=500)
