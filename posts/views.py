#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Vistas de la app `posts`.
#
# Incluye:
# - post_list: render del listado con ordenación por fecha desc.
# - healthz: ping de salud del runtime Django.
# - db_healthz: ping de salud a la BD (SELECT 1).

from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Post
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import get_template


def post_list(request):
    # Consulta las entradas y aplica orden cronológico inverso (más nuevas primero).
    # El modelo ya define Meta.ordering, pero mantenemos el order_by explícito por claridad.
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


def static_healthz(request):
    """Comprueba que el almacenamiento de estáticos puede resolver una URL.

    Útil en producción (DEBUG=False) para diagnosticar problemas de manifest
    (MissingManifestEntry) sin renderizar plantillas.
    """
    try:
        url = staticfiles_storage.url('post/style.css')
        return JsonResponse({"ok": True, "url": url})
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=500)


def template_debug(request):
    """Diagnóstico de plantillas/estáticos ejecutado desde Django.

    - Intenta resolver la URL estática del CSS vía storage (manifest).
    - Intenta cargar la plantilla 'posts/index.html' y, si puede, la renderiza
      con un contexto mínimo (sin tocar BD) para detectar errores de carga.
    - Devuelve JSON con el resultado o la excepción capturada.
    """
    data = {"ok": True}
    # Comprobar estático via storage (usa manifest en prod)
    try:
        data["static_url"] = staticfiles_storage.url('post/style.css')
    except Exception as exc:
        data.update({"ok": False, "static_error": str(exc)})

    # Comprobar carga y render de plantilla
    try:
        tpl = get_template('posts/index.html')
        # Render sin hits a la BD: pasamos posts=[]
        _ = tpl.render({"posts": []}, request)
        data["template"] = "ok"
    except Exception as exc:
        data.update({"ok": False, "template_error": str(exc)})

    status = 200 if data.get("ok") else 500
    return JsonResponse(data, status=status)
