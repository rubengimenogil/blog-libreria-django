from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Post

def post_list(request):
    """Renderiza la home con el listado de posts.

    Paso a paso para un aprendiz:
    1) Consultamos los posts desde la base de datos con el ORM.
    2) Los ordenamos de más nuevos a más antiguos (order_by desc),
       aunque `Meta.ordering` ya lo hace: aquí lo dejamos explícito por didáctica.
    3) Llamamos a `render` para combinar plantilla + contexto y obtener HTML.
    """
    # 1 y 2) Query + orden
    posts = Post.objects.all().order_by('-published_date')
    # 3) Render de la plantilla
    return render(request, 'posts/index.html', {'posts': posts})

def healthz(request):
    """Responde si la app está viva sin tocar la BD (útil para checks rápidos)."""
    return JsonResponse({"ok": True})

def db_healthz(request):
    """Comprueba conectividad a la base de datos ejecutando SELECT 1.

    Devuelve 200 si la conexión funciona; 500 si hay error de conexión/SSL/credenciales.
    """
    try:
        # Abrimos un cursor crudo a la BD y ejecutamos una sentencia trivial
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
        return JsonResponse({"ok": True, "db": True, "result": row[0] if row else None})
    except Exception as exc:
        # Si algo falla (credenciales, SSL, etc.), devolvemos 500 con el error
        return JsonResponse({"ok": False, "db": False, "error": str(exc)}, status=500)
