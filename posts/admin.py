#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Configuración del panel de administración para el modelo Post.
#
# Consejos:
# - list_display: columnas visibles en la lista.
# - search_fields: campos con búsqueda de texto.
# - ordering: orden por defecto (coincide con el del modelo).

from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "published_date")
	search_fields = ("title", "content")
	ordering = ("-published_date",)
